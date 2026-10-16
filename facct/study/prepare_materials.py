"""Deterministic session preparation; never fabricates participant outcomes."""
import hashlib
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SEED = 20261003
DOMAINS = ("education", "health", "mental_health")
CRITERIA = ("D_ge3", "F_lt4", "OA_lt4")
POLICIES = {"A": "high_H", "B": "length", "C": "markers"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key(value):
    return hashlib.sha256(f"{SEED}|{value}".encode()).hexdigest()


def case_id(value):
    return hashlib.sha256(("blind|" + value).encode()).hexdigest()[:12]


def rotate(items, n):
    n %= len(items)
    return list(items[n:]) + list(items[:n])


def choose_cases(frame, register):
    orientation = sorted(frame.id, key=key)[:2]
    cells = {}
    for r in register.itertuples():
        if pd.isna(r.id):
            continue
        cells.setdefault(r.id, set()).update((f"criterion:{r.criterion}:{r.status}", f"policy:{r.policy}:{r.status}"))
    diagnostic, covered = [], set()
    while len(diagnostic) < min(6, len(cells)):
        candidates = [i for i in cells if i not in diagnostic]
        chosen = min(candidates, key=lambda i: (-len(cells[i] - covered), key(i)))
        diagnostic.append(chosen)
        covered |= cells[chosen]
    return orientation, diagnostic, sorted(covered), sorted(set().union(*cells.values()) - covered)


def verbatim(text):
    fences = re.findall(r"`+", str(text))
    fence = "`" * max(3, 1 + max(map(len, fences), default=0))
    return f"{fence}text\n{text}\n{fence}"


def cases_document(title, ids, source):
    lines = [f"# {title}", "", "Preparation draft. Share only at the designated session stage after approved consent. You may skip any case or stop. These are research examples, not advice.", ""]
    for value in ids:
        r = source.loc[value]
        lines += [f"## Case {case_id(value)}", "", "Prompt", "", verbatim(r.prompt), "", "Response", "", verbatim(r.response), "", "Would you allocate a review slot, decline review, or need more information? Please explain what matters in this situation.", ""]
    return "\n".join(lines)


def evidence_document(domain, slot, order, criterion_order, table):
    lines = [f"# {domain}: evidence panels for planned slot {slot}", "", "Do not show until initial and blind-case notes are locked. This is an exploratory screening simulation using existing ratings, not established organizational practice. A response outside a criterion is not necessarily safe. Non-selection means unreviewed, not cleared.", "",
             "All policies have the same exact review capacity. D >= 3 denotes a broad anthropomorphic-implication review trigger (including simulated affect/understanding); F < 4 means below strong domain fit; OA < 4 means below mostly appropriate. These use five-rater means, not observed harm outcomes. Criteria are contestable, not interchangeable.", ""]
    for criterion in criterion_order:
        g = table[(table.domain == domain) & (table.criterion == criterion) & (table.budget == .2)].set_index("policy")
        first = g.loc["high_H"]
        lines += [f"## {criterion}", "", f"Batch: {int(first.n)} responses. Criterion cases: {int(first.concerns)} in {int(first.concern_clusters)} prompt clusters. Review capacity: {int(first.selected)} responses.", "",
                  "| Policy | Cases selected / criterion cases | Precision | Recall (pointwise 95% CI) | Criterion cases unreviewed |", "|---|---:|---:|---|---:|"]
        for alias in order:
            row = g.loc[POLICIES[alias]]
            lines.append(f"| {alias} | {int(row.caught)}/{int(row.concerns)} | {100*row.precision:.1f}% | {100*row.recall:.1f}% [{100*row.recall_lo:.1f}, {100*row.recall_hi:.1f}] | {int(row.missed)} |")
        random = g.loc["uniform_random"]
        lines += ["", f"Exact-size uniform random selection: expected {random.caught:.2f} criterion cases selected, expected recall {100*random.recall:.1f}%, expected precision {100*random.precision:.1f}%. Fractional counts are expectations across random draws, not a possible observed count in one draw.", "",
                  "Describe what recall and precision mean here. What can be concluded about an unselected response? What would you challenge about this criterion or decision?", ""]
    lines += ["Intervals use 2,000 prompt-cluster resamples and fixed released ratings. They do not cover uncertainty about the appropriateness of a criterion or a different rater/deployment population. Undefined resamples are reported in the accompanying study analysis. Pointwise intervals are not simultaneous policy-comparison tests. The author/intern dimension-rating pool was framework-familiar; OA came from separate domain pools. This is not independent harm validation.", "", "Policy definitions will be explained after the initial teach-back. You may revise or dispute your interpretation; initial and later responses are recorded separately."]
    return "\n".join(lines) + "\n"


def prepare(root=ROOT, output=None):
    output = output or root / "facct/study/materials"
    output.mkdir(parents=True, exist_ok=True)
    paths = [root / "analysis/processed/persona_all.csv", root / "facct/outputs/tables/case_sampling_register.csv", root / "facct/outputs/tables/screening.csv", root / "facct/study/session_plan.md"]
    before = {str(p.relative_to(root)): digest(p) for p in paths}
    d = pd.read_csv(paths[0])
    d["id"] = d.domain + ":" + d.annotation_item_id
    source = d.set_index("id")
    register = pd.read_csv(paths[1])
    results = pd.read_csv(paths[2])
    schedule, sampled, coverage, answers = [], [], [], []
    for offset, domain in enumerate(DOMAINS):
        g = d[d.domain == domain]
        orientation, diagnostic, covered, uncovered = choose_cases(g, register[register.domain == domain])
        assert len(orientation) == 2 and len(diagnostic) == 6
        coverage.append(dict(domain=domain, covered_cells=covered, uncovered_cells=uncovered, orientation_diagnostic_overlap=sorted(set(orientation) & set(diagnostic))))
        for stage, ids in (("orientation", orientation), ("diagnostic", diagnostic)):
            for value in ids:
                row = source.loc[value]
                flags = sorted(set(re.findall(r"\b(?:chatgpt|gpt|claude|glm|openai|anthropic)\b", row.prompt + "\n" + row.response, flags=re.I)))
                sampled.append(dict(domain=domain, stage=stage, case_id=case_id(value), source_id=value, identity_strings_to_review=";".join(flags), human_blinding_review_status="pending"))
        for slot in range(1,4):
            code = f"{domain}_{slot}"
            order = rotate(list(POLICIES), offset + slot - 1)
            criteria = rotate(list(CRITERIA), offset + 2*(slot-1))
            oi = rotate(orientation, slot-1)
            di = rotate(diagnostic, 2*(slot-1))
            schedule.append(dict(planned_slot=code, status="not enrolled", target="initial target" if slot<3 else "availability-based optional", policy_order=" ".join(order), criterion_order=" ".join(criteria), orientation_case_order=" ".join(map(case_id,oi)), diagnostic_case_order=" ".join(map(case_id,di))))
            folder = output / code
            folder.mkdir(exist_ok=True)
            (folder / "part1_orientation.md").write_text(cases_document("Part 1: orientation cases", oi, source))
            (folder / "part2_blind_cases.md").write_text(cases_document("Part 2: blind diagnostic cases", di, source))
            (folder / "part3_evidence.md").write_text(evidence_document(domain,code,order,criteria,results))
        for criterion in CRITERIA:
            row = results[(results.domain==domain)&(results.criterion==criterion)&(results.policy=="high_H")&(results.budget==.2)].iloc[0]
            answers += [f"### {domain}, {criterion}, policy A", f"Review capacity {int(row.selected)}/{int(row.n)}; criterion cases selected {int(row.caught)}/{int(row.concerns)}. Recall denominator = criterion cases ({int(row.concerns)}); precision denominator = selected responses ({int(row.selected)}). Unreviewed criterion cases = {int(row.missed)}.", ""]
    pd.DataFrame(schedule).to_csv(output/"planned_slots.csv",index=False)
    pd.DataFrame(sampled).to_csv(output/"coordinator_case_register.csv",index=False)
    (output/"sampling_coverage.json").write_text(json.dumps(coverage,indent=2)+"\n")
    key_text = ["# Facilitator answer key (NOT participant data)", "", "Keep separate from participant-facing materials. Do not score normative disagreement as arithmetic misunderstanding. Record initial teach-back responses before explaining.", "", "Policy mapping: A = descending HumT; B = descending response word count; C = descending proportion of the predefined pronoun/conversational markers. This is not randomized treatment assignment. Explain each policy after initial teach-back, without calling any policy best.", "", "Non-selection does not establish safety. Random values are analytical expectations, not one observed draw. Bootstrap intervals concern fixed-label corpus sampling, not uncertainty about who should set the criterion, experienced harm or new populations.", "", *answers]
    (output/"facilitator_answer_key.md").write_text("\n".join(key_text)+"\n")
    (output/"README.md").write_text("# Prepared session packets\n\nNOT APPROVED OR CONDUCTED. Nine planned slots are not nine participants. Six initial slots and three availability-based optional slots implement the author's confirmed three-domain plan.\n\nShare the three parts only at their specified stages in session_plan.md. Keep planned_slots.csv, coordinator_case_register.csv, sampling_coverage.json and facilitator_answer_key.md away from participant screens. Do not place completed notes, consent, contact details or recordings here.\n\nSampling is deterministic but purposive for the diagnostic block, not prevalence-representative. Orientation selection ignores labels and policy status. The coverage record discloses omitted cells and repeated cases. Human review of text, identity hints and timing is pending; algorithmic flagging is not approval.\n\nTo regenerate: `python -m facct.study.prepare_materials`. Source data and computational outputs are not modified.\n")
    assert before == {str(p.relative_to(root)): digest(p) for p in paths}
    manifest = dict(version="1.1",seed=SEED,orientation_rule="two smallest SHA256(seed|domain:item ID) from full domain corpus; no labels",diagnostic_rule="greedy six-case coverage of existing criterion/status and policy/status sampling cells; seeded tie-break",human_participants=0,status="preparation only",source_hashes=before,generator_sha256=digest(Path(__file__)),generated_files={str(p.relative_to(output)):digest(p) for p in sorted(output.rglob("*")) if p.is_file() and p.name!="manifest.json"})
    (output/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    return manifest


if __name__ == "__main__":
    result = prepare()
    print(f"Prepared {len(result['generated_files'])} files; 0 human participants; source hashes unchanged.")
