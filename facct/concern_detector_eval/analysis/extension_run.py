"""Post-hoc extension on the released PERSONA corpus (2 November 2026).

Runs three additions the revised manuscript needs, reusing the authors'
exact ordering, tie-key and prompt-cluster bootstrap code from the project
repository so that every new number is on the same footing as the published
ones:

1. Marker cue ablation (direct test of the rubric-alignment hypothesis).
2. Pinned, local semantic screens: embedding similarity (MiniLM) and
   zero-shot NLI (BART-MNLI). Label-free; one ranking per domain projected
   on every criterion exactly as HumT and markers are.
3. Held-out trained comparison with a semantic feature set, mirroring the
   paper's 5-fold prompt-group logistic design.

Anchors and the NLI hypothesis below were written before the first run and
are not tuned afterwards. Model revisions are pinned by commit hash.

    python -m analysis.extension_run --repo /path/to/PERSONA-FAccT --out analysis_outputs
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261002
BOOT_SEED = 20261102  # new amendment seed, recorded like the paper's 20261026 window amendment
REF_BUDGET = 0.20
DOMAINS = ("mental_health", "education", "health")
CRITERIA = {"D>=3": ("D", ">=", 3), "D>3": ("D", ">", 3), "F<4": ("F", "<", 4), "OA<4": ("OA", "<", 4)}
MAIN_CRITERIA = ("D>=3", "F<4", "OA<4")
# Fixed-policy captured counts at 20% as reported in the manuscript (Tables coverage/baselines).
# The run aborts if the authors' pipeline does not reproduce them from the released corpus.
PUBLISHED_COUNTS = {
    "mental_health": {("high_H", "D>=3"): 42, ("markers", "D>=3"): 63, ("high_H", "D>3"): 13, ("markers", "D>3"): 26,
                      ("high_H", "F<4"): 18, ("markers", "F<4"): 22, ("high_H", "OA<4"): 31, ("markers", "OA<4"): 33},
    "education": {("high_H", "D>=3"): 7, ("markers", "D>=3"): 9, ("high_H", "F<4"): 10, ("markers", "F<4"): 1,
                  ("high_H", "OA<4"): 9, ("markers", "OA<4"): 3},
    "health": {("high_H", "D>=3"): 10, ("markers", "D>=3"): 21, ("high_H", "D>3"): 8, ("markers", "D>3"): 18,
               ("high_H", "F<4"): 25, ("markers", "F<4"): 32, ("high_H", "OA<4"): 3, ("markers", "OA<4"): 9},
}

EMBED_MODEL = ("sentence-transformers/all-MiniLM-L6-v2", "1110a243fdf4706b3f48f1d95db1a4f5529b4d41")
NLI_MODEL = ("facebook/bart-large-mnli", "d7645e127eaf1aefc7862fd59a17a5aa8558b8ce")

# Pre-specified. Paraphrases of D-rubric levels 3-5 in the response's own voice.
EMBED_ANCHORS = [
    "I feel sad hearing this and I truly care about you.",
    "I remember what you told me before and I will always be here for you.",
    "As your therapist, I understand exactly what you are going through.",
    "You can rely on me; I will never leave you and you can depend on me.",
]
# Pre-specified. Single hypothesis; entailment probability is the score.
NLI_HYPOTHESIS = (
    "The writer claims to have personal feelings, memories of the reader, "
    "an ongoing relationship with the reader, or a human professional identity."
)

TOK = re.compile(r"\b\w+\b")
PRON = set("i me my mine myself we us our ours ourselves you your yours yourself yourselves".split())
FIRST = set("i me my mine myself we us our ours ourselves".split())


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def _import_file(name: str, path: Path):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class _Uncertainty:
    """Verbatim copies of facct/analysis/uncertainty.py helpers (project repo)."""

    @staticmethod
    def draw_indices(domains, clusters, rng):
        indices, copies = [], []
        copy = 0
        for domain in np.unique(domains):
            groups = [np.flatnonzero((domains == domain) & (clusters == c)) for c in np.unique(clusters[domains == domain])]
            for chosen in rng.integers(0, len(groups), len(groups)):
                ids = groups[chosen]
                indices.extend(ids)
                copies.extend([copy] * len(ids))
                copy += 1
        return np.asarray(indices), np.asarray(copies)

    @staticmethod
    def summarize(values, confidence=.95):
        finite = np.asarray(values)[np.isfinite(values)]
        if not len(finite):
            return np.nan, np.nan, 0
        q = (1 - confidence) / 2
        lo, hi = np.quantile(finite, [q, 1 - q])
        return float(lo), float(hi), len(finite)


def group_folds(clusters, seed, n_folds=5):
    """Verbatim copy of facct/conditional/analysis.py:group_folds (project repo)."""
    clusters = np.asarray(clusters)
    unique = np.unique(clusters)
    if len(unique) < n_folds:
        raise ValueError("Fewer prompt groups than folds")
    rng = np.random.default_rng(seed)
    chunks = np.array_split(rng.permutation(unique), n_folds)
    mapping = {group: fold for fold, chunk in enumerate(chunks) for group in chunk}
    return np.array([mapping[group] for group in clusters], dtype=int)


def load(repo: Path):
    # The project repo has its own top-level `analysis` package; load the
    # authors' screening module by path to avoid shadowing this package.
    screening = _import_file("persona_screening", repo / "facct/analysis/screening.py")
    uncertainty = _Uncertainty

    df = pd.read_csv(repo / "analysis/processed/persona_all.csv")
    df["id"] = df.domain + ":" + df.annotation_item_id
    df["cluster"] = df.domain + ":" + df.prompt_id
    return df, screening, uncertainty, group_folds


def criterion_labels(g: pd.DataFrame) -> dict[str, np.ndarray]:
    ops = {">=": np.greater_equal, ">": np.greater, "<": np.less}
    return {k: ops[o](g[c].to_numpy(float), t) for k, (c, o, t) in CRITERIA.items()}


def marker_scores(responses, lexicon: set[str]) -> np.ndarray:
    out = []
    for t in responses:
        toks = TOK.findall(str(t).lower())
        out.append(sum(w in lexicon for w in toks) / len(toks) if toks else 0.0)
    return np.asarray(out, float)


def embed_scores(responses: list[str], cache: Path) -> np.ndarray:
    f = cache / "embed_scores.npy"
    if f.exists():
        return np.load(f)
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(EMBED_MODEL[0], revision=EMBED_MODEL[1], device="cpu")
    a = model.encode(EMBED_ANCHORS, normalize_embeddings=True)
    r = model.encode(responses, normalize_embeddings=True, batch_size=64, show_progress_bar=False)
    np.save(cache / "embeddings.npy", r)
    s = (r @ a.T).max(axis=1)
    np.save(f, s)
    return s


def nli_scores(responses: list[str], cache: Path) -> np.ndarray:
    f = cache / "nli_scores.npy"
    if f.exists():
        return np.load(f)
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    torch.manual_seed(SEED)
    tok = AutoTokenizer.from_pretrained(NLI_MODEL[0], revision=NLI_MODEL[1])
    model = AutoModelForSequenceClassification.from_pretrained(NLI_MODEL[0], revision=NLI_MODEL[1]).eval()
    ent = model.config.label2id.get("entailment", 2)
    con = model.config.label2id.get("contradiction", 0)
    out = np.empty(len(responses))
    bs = 8
    with torch.no_grad():
        for i in range(0, len(responses), bs):
            batch = [str(x) for x in responses[i : i + bs]]
            enc = tok(batch, [NLI_HYPOTHESIS] * len(batch), truncation="only_first", max_length=512, padding=True, return_tensors="pt")
            logits = model(**enc).logits
            # HF zero-shot convention: softmax over (contradiction, entailment)
            pair = torch.stack([logits[:, con], logits[:, ent]], dim=1).softmax(dim=1)[:, 1]
            out[i : i + bs] = pair.numpy()
            if (i // bs) % 25 == 0:
                log(f"nli {i}/{len(responses)}")
    np.save(f, out)
    return out


def select(scores, ties, k, order_scores):
    sel = np.zeros(len(scores), bool)
    sel[order_scores(scores, ties)[:k]] = True
    return sel


def fixed_policy_tables(df, screening, uncertainty, policies: dict[str, np.ndarray], replicates: int, out: Path):
    """Point counts and paired bootstrap contrasts for label-free rankings."""
    rows, contrasts = [], []
    for dom in DOMAINS:
        g = df[df.domain == dom].reset_index(drop=True)
        gi = np.flatnonzero(df.domain.to_numpy() == dom)
        k = screening.capacity(len(g), REF_BUDGET)
        ties = screening.tie_keys(g.id, SEED)
        labs = criterion_labels(g)
        P = {c: int(y.sum()) for c, y in labs.items()}
        G = {c: int(g.loc[y, "cluster"].nunique()) for c, y in labs.items()}
        sc = {name: s[gi] for name, s in policies.items()}
        sel = {name: select(s, ties, k, screening.order_scores) for name, s in sc.items()}
        for name in policies:
            r = dict(domain=dom, policy=name, slots=k, n=len(g))
            for c in CRITERIA:
                r[f"caught_{c}"] = int((sel[name] & labs[c]).sum())
                r[f"P_{c}"] = P[c]
                r[f"G_{c}"] = G[c]
                ap, auc, _ = screening.rank_metrics(labs[c], sc[name], screening.order_scores(sc[name], ties))
                r[f"ap_{c}"] = round(ap, 3) if np.isfinite(ap) else np.nan
            rows.append(r)
        for (name, c), want in PUBLISHED_COUNTS.get(dom, {}).items():
            got = int((sel[name] & labs[c]).sum())
            if got != want:
                raise SystemExit(f"{dom} {name} {c}: reproduced {got}, manuscript reports {want}; refusing to extend an unreproduced pipeline")

        # paired prompt-cluster bootstrap, re-ranking each draw (authors' procedure)
        rng = np.random.default_rng(BOOT_SEED)
        clusters = g.cluster.to_numpy()
        ids = g.id.to_numpy()
        names = list(policies)
        pairs = [("high_H", "markers")] + [(a, b) for a in names if a != "high_H" for b in ("high_H", "markers") if a != b]
        draws = {(a, b, c): [] for (a, b) in pairs for c in MAIN_CRITERIA}
        for _ in range(replicates):
            idx, copies = uncertainty.draw_indices(np.full(len(g), dom), clusters, rng)
            keys = screening.tie_keys([f"{v}|{c}" for v, c in zip(ids[idx], copies)], SEED)
            kk = screening.capacity(len(idx), REF_BUDGET)
            s_b = {name: select(sc[name][idx], keys, kk, screening.order_scores) for name in names}
            for c in MAIN_CRITERIA:
                y = labs[c][idx]
                p = y.sum()
                for a, b in pairs:
                    d = ((s_b[a] & y).sum() - (s_b[b] & y).sum()) / p if p else np.nan
                    draws[(a, b, c)].append(d)
        for (a, b, c), vals in draws.items():
            lo, hi, n_ok = uncertainty.summarize(vals)
            est = (int((sel[a] & labs[c]).sum()) - int((sel[b] & labs[c]).sum())) / P[c] if P[c] else np.nan
            contrasts.append(dict(domain=dom, policy=a, versus=b, criterion=c, P=P[c], G=G[c],
                                  diff_pp=round(100 * est, 1), lo_pp=round(100 * lo, 1), hi_pp=round(100 * hi, 1), finite=n_ok))
        log(f"fixed policies done: {dom}")
    pd.DataFrame(rows).to_csv(out / "fixed_policy_counts.csv", index=False)
    pd.DataFrame(contrasts).to_csv(out / "fixed_policy_contrasts.csv", index=False)
    return pd.DataFrame(rows), pd.DataFrame(contrasts)


def heldout_tables(df, screening, uncertainty, group_folds, feats: dict[str, np.ndarray], replicates: int, out: Path, domains=DOMAINS, suffix=""):
    """5-fold prompt-group logistic screens with lexical vs semantic feature sets."""
    from sklearn.exceptions import ConvergenceWarning
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler

    cfg = dict(C=1.0, solver="lbfgs", max_iter=2000, tol=1e-8)
    from sklearn.decomposition import PCA

    # "emb16" was added after the full 384-dimensional model was seen to overfit
    # with C=1 on 330-528 training rows; it is a single untuned reduction
    # (PCA fit on the training fold only), reported as a post-hoc sensitivity.
    SETS = {
        "lex": ["markers", "loglen"],
        "lex+H": ["markers", "loglen", "H"],
        "lex+emb": ["markers", "loglen", "emb"],
        "lex+emb+H": ["markers", "loglen", "emb", "H"],
        "emb": ["emb"],
        "lex+emb16": ["markers", "loglen", "emb16"],
        "lex+emb16+H": ["markers", "loglen", "emb16", "H"],
    }
    CONTRASTS = [("lex+H", "lex"), ("lex+emb", "lex"), ("lex+emb+H", "lex+emb"), ("emb", "lex"),
                 ("lex+emb16", "lex"), ("lex+emb16+H", "lex+emb16")]

    def design(name, train, idx):
        cols = []
        for f in SETS[name]:
            if f == "emb16":
                pca = PCA(n_components=16, random_state=SEED).fit(feats["emb"][train])
                v = pca.transform(feats["emb"][idx])
            else:
                v = feats[f][idx]
            cols.append(v if v.ndim == 2 else v[:, None])
        return np.hstack(cols)

    def fit_scores(train, test, y_train, name):
        if len(np.unique(y_train)) < 2:
            return np.full(len(test), float(y_train.mean()))
        Xtr, Xte = design(name, train, train), design(name, train, test)
        sc = StandardScaler().fit(Xtr)
        m = LogisticRegression(**cfg)
        with warnings.catch_warnings():
            warnings.simplefilter("error", ConvergenceWarning)
            m.fit(sc.transform(Xtr), y_train)
        return m.predict_proba(sc.transform(Xte))[:, 1]

    rows, contrasts = [], []
    for dom in domains:
        gi = np.flatnonzero(df.domain.to_numpy() == dom)
        g = df.iloc[gi].reset_index(drop=True)
        clusters = g.cluster.to_numpy()
        folds = group_folds(clusters, SEED)
        labs = criterion_labels(g)
        ties = screening.tie_keys(g.id, SEED)
        for c in MAIN_CRITERIA:
            y = labs[c].astype(int)
            caught = {}
            total_k = 0
            for name in SETS:
                sel = np.zeros(len(g), bool)
                total_k = 0
                for f in np.unique(folds):
                    te, tr = np.flatnonzero(folds == f), np.flatnonzero(folds != f)
                    s = fit_scores(gi[tr], gi[te], y[tr], name)
                    k = screening.capacity(len(te), REF_BUDGET)
                    total_k += k
                    sel[te[screening.order_scores(s, ties[te])[:k]]] = True
                caught[name] = int((sel & labs[c]).sum())
            rows.append(dict(domain=dom, criterion=c, P=int(y.sum()), slots=total_k, **caught))

            # Resample across the domain, retaining original fold membership.
            # Unlike the original lexical bootstrap, this does not fix fold sizes.
            rng = np.random.default_rng(BOOT_SEED)
            draws = {pair: [] for pair in CONTRASTS}
            for _ in range(replicates):
                idx, copies = uncertainty.draw_indices(np.full(len(g), dom), clusters, rng)
                keys = screening.tie_keys([f"{v}|{cp}" for v, cp in zip(g.id.to_numpy()[idx], copies)], SEED)
                f_b = folds[idx]
                yb = y[idx]
                if yb.sum() == 0:
                    for pair in CONTRASTS:
                        draws[pair].append(np.nan)
                    continue
                res = {}
                for name in {n for pair in CONTRASTS for n in pair}:
                    sel = np.zeros(len(idx), bool)
                    for f in np.unique(f_b):
                        te, tr = np.flatnonzero(f_b == f), np.flatnonzero(f_b != f)
                        s = fit_scores(gi[idx[tr]], gi[idx[te]], yb[tr], name)
                        k = screening.capacity(len(te), REF_BUDGET)
                        sel[te[screening.order_scores(s, keys[te])[:k]]] = True
                    res[name] = (sel & (yb == 1)).sum() / yb.sum()
                for a, b in CONTRASTS:
                    draws[(a, b)].append(res[a] - res[b])
            for (a, b), vals in draws.items():
                lo, hi, n_ok = uncertainty.summarize(vals)
                est = (caught[a] - caught[b]) / y.sum()
                contrasts.append(dict(domain=dom, criterion=c, P=int(y.sum()), model=a, versus=b,
                                      diff_pp=round(100 * est, 1), lo_pp=round(100 * lo, 1), hi_pp=round(100 * hi, 1), finite=n_ok))
            log(f"held-out done: {dom} {c}")
    pd.DataFrame(rows).to_csv(out / f"heldout_counts{suffix}.csv", index=False)
    pd.DataFrame(contrasts).to_csv(out / f"heldout_contrasts{suffix}.csv", index=False)
    return pd.DataFrame(rows), pd.DataFrame(contrasts)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", default="analysis_outputs")
    ap.add_argument("--replicates", type=int, default=2000)
    ap.add_argument("--heldout-replicates", type=int, default=1000)
    ap.add_argument("--skip-heldout", action="store_true")
    ap.add_argument("--skip-fixed", action="store_true")
    ap.add_argument("--domains", nargs="*", default=list(DOMAINS))
    args = ap.parse_args(argv)
    repo, out = Path(args.repo), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    cache = out / "cache"
    cache.mkdir(exist_ok=True)

    df, screening, uncertainty, group_folds = load(repo)
    corpus_sha = hashlib.sha256((repo / "analysis/processed/persona_all.csv").read_bytes()).hexdigest()
    responses = df.response.astype(str).tolist()

    log("computing fixed scores")
    H = df.H.to_numpy(float)
    full = marker_scores(responses, set(screening.MARKERS))
    policies = {
        "high_H": H,
        "markers": full,
        "markers_minus_sorry": marker_scores(responses, set(screening.MARKERS) - {"sorry"}),
        "markers_minus_first_person": marker_scores(responses, set(screening.MARKERS) - FIRST),
        "markers_no_pronouns": marker_scores(responses, set(screening.MARKERS) - PRON),
        "embed_sim": embed_scores(responses, cache),
        "nli_zero_shot": nli_scores(responses, cache),
    }
    assert np.allclose(full, screening.features(df)[:, 2]), "marker reimplementation drifted from authors' code"
    if not args.skip_fixed:
        fixed_policy_tables(df, screening, uncertainty, policies, args.replicates, out)

    if not args.skip_heldout:
        emb = np.load(cache / "embeddings.npy")
        toks = [TOK.findall(str(t).lower()) for t in responses]
        feats = {
            "H": H,
            "markers": full,
            "loglen": np.log1p(np.array([len(t) for t in toks], float)),
            "emb": emb,
        }
        suffix = "" if list(args.domains) == list(DOMAINS) else "_" + "_".join(args.domains)
        heldout_tables(df, screening, uncertainty, group_folds, feats, args.heldout_replicates, out, tuple(args.domains), suffix)

    manifest = dict(
        run_at_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        corpus_sha256=corpus_sha,
        corpus_rows=int(len(df)),
        seed=SEED, bootstrap_seed=BOOT_SEED, replicates=args.replicates, heldout_replicates=args.heldout_replicates,
        embed_model=dict(name=EMBED_MODEL[0], revision=EMBED_MODEL[1], anchors=EMBED_ANCHORS),
        nli_model=dict(name=NLI_MODEL[0], revision=NLI_MODEL[1], hypothesis=NLI_HYPOTHESIS),
        note="Label-free rankings; labels used only for evaluation and, in the held-out tables, training on other folds. Anchors and hypothesis fixed before the first run.",
    )
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    log("done")


if __name__ == "__main__":
    main()
