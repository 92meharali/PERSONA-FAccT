# HumT review-prioritization audit — revision package

## Current revision (3 November 2026)

The active paper incorporates the professor's feedback: clearer story and
method, expanded verified related work, self-contained PERSONA profile,
editable ACM-style workflow, results figure, corrected claims and complete
semantic comparisons against the independent follow-up. See
`notes/professor_revision_response.md` for every change and remaining author
decisions. Follow-up compensation was confirmed as existing paid research roles
on 3 November 2026; the endmatter placeholder is resolved.

Reproduce the new computational work without model calls:

```bash
python -m analysis.run_professor_revision --repo /path/to/PERSONA-FAccT --study /path/to/independent_annotation_study
```

Use an environment with NumPy, pandas, SciPy, scikit-learn, Matplotlib and
pytest. The 2,000-draw cached-score analysis took about nine seconds locally;
tables, figures and tests normally take a few additional seconds. Existing
corpus/score hashes, unique IDs and all original queue memberships are checked
before the extension. Private study inputs are read in place, never packaged.
The current Overleaf package is under `releases/`; its manifest records the
actual compiled page counts. Previous revision history follows below and is
not the current submission checklist.

## Previous revision history

Revision of *When Tone Scores Allocate Attention: A Use-Validity Audit of
HumT-Based Review Prioritization* (FAccT 2027 submission) in response to nine
review concerns, plus the analysis code and outputs for the data-backed
amendment (cue ablation, pinned semantic comparators, embedding-augmented
held-out screens) run on the project repository
(`github.com/92meharali/PERSONA-FAccT`).

```
paper/                      LaTeX source (Overleaf-ready), tables, figures, compiled main.pdf
RESPONSE_TO_REVIEWERS.md    point-by-point: what changed, what it rests on, what remains
analysis/                   extension runner, table/figure generators, standalone tools
analysis_outputs/           amendment results: CSVs, manifest.json, cached model scores
tests/                      unit tests for the toolkit
```

## Building the paper

```bash
cd paper
tectonic -X compile main.tex        # or pdflatex + bibtex, or upload the folder to Overleaf
```

The manuscript compiles with no errors, undefined references or overfull
boxes. Main text is 14 pages (the FAccT 2027 limit), followed by one endmatter
page, references and appendices.

## Reproducing the amendment

```bash
uv venv .venv && . .venv/bin/activate
uv pip install -r requirements.txt
git clone https://github.com/92meharali/PERSONA-FAccT /tmp/persona-src

# fixed policies (cue ablation + semantic screens), 2,000 paired bootstrap draws
python -m analysis.extension_run --repo /tmp/persona-src --out analysis_outputs --replicates 2000 --skip-heldout
# held-out trained screens, 1,000 refitted draws, one process per domain
for d in mental_health education health; do
  python -m analysis.extension_run --repo /tmp/persona-src --out analysis_outputs --skip-fixed \
      --heldout-replicates 1000 --domains $d &
done; wait
python -m analysis.make_extension_tables analysis_outputs paper/tables
python -m analysis.make_alignment_figure          # paper/figures/alignment_diagnostic.pdf
```

`extension_run.py` imports the authors' `facct/analysis/screening.py` by path
and reuses their seed (20261002), SHA-256 tie keys, exact floor capacities and
prompt-group folds; it asserts that every original fixed-policy count is
reproduced before adding policies. Model scores are cached in
`analysis_outputs/cache/` (first run downloads `all-MiniLM-L6-v2` and
`bart-large-mnli` at the pinned revisions; NLI scoring takes ~8 min on CPU).
`analysis_outputs/manifest.json` records corpus hash, seeds, model revisions,
anchors and hypothesis. Bootstrap draws use seed 20261102, so amendment
intervals for the original HumT–marker contrasts differ from the paper's
original ones by resampling noise; point estimates match exactly.

## Standalone tools

The modules below are general-purpose and run on CSV inputs. Install as above, then:

```bash
python -m pytest -q
```

| Module | Review concern | What it does | Needs |
|---|---|---|---|
| `analysis.paired_detection` | 3, 7 | Exact McNemar, Wilson CIs, Beta posterior over every feasible overlap, prompt-cluster bootstrap, replication size. Reproduces the paper's follow-up numbers from counts alone. | nothing (`--counts 19 12 6`) or a flags CSV |
| `analysis.cue_overlap` | 2 | Ablates rubric-overlapping cues (or a cue category) from the 23-word marker list and re-ranks at exact capacity. | responses CSV with `response`, `positive` |
| `analysis.semantic_comparator` | 4 | Pinned, cached LLM-judge or embedding screen with run manifest (model id, prompt version, decoding, input hashes). `--provider mock` for dry runs. | responses CSV with `prompt`, `response`; API key for `openai` |
| `analysis.score_audit` | 5 | Historical-vs-rescored HumT: text provenance tiers, agreement statistics, and whether the 132-slot selection and captured positives change. | table with historical and rescored scores (+ texts) |

Examples:

```bash
# follow-up inference from the reported counts (no data needed)
python -m analysis.paired_detection --counts 19 12 6 --a markers --b humt

# with per-response flags and prompt clusters
python -m analysis.paired_detection --csv data/followup_flags.csv --a markers --b humt

# cue ablation at the mental-health reference capacity
python -m analysis.cue_overlap --responses data/mh.csv --rubric prompts/rubric_D.txt \
    --capacity 132 --drop-category sympathy --humt humt_recorded

# semantic comparator dry run, then a pinned judge
python -m analysis.semantic_comparator --responses data/mh.csv --criterion prompts/reviewworthiness.md \
    --provider mock --out out/mock.csv
OPENAI_API_KEY=... python -m analysis.semantic_comparator --responses data/mh.csv \
    --criterion prompts/reviewworthiness.md --provider openai --model gpt-4o-2024-08-06 --out out/judge.csv
```

Input schemas are documented in each module's docstring. Labels are never
read by the scoring modules; evaluation happens in `paired_detection`.
