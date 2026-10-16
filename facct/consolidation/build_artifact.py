"""Build and smoke-test a local code/aggregate candidate without raw source text."""
import csv
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

from .audit import ROOT
from facct.analysis.validate_inputs import sha

EXCLUDED_COLUMNS = {"prompt", "response", "text", "annotator_id", "rater_id"}
IDENTITY = re.compile(r"/Users/|92meharali|PERSONA-MH-CHI|meharali|junaid|ghaznavi|allama iqbal", re.I)


def safe_csv(path):
    with path.open() as stream:
        columns = set(next(csv.reader(stream)))
    return not (columns & EXCLUDED_COLUMNS) and not path.name.startswith(("cases_", "case_", "human_coding"))


def payload():
    files = {}
    for folder in ("facct/analysis", "facct/revision", "facct/conditional", "facct/allocation"):
        for path in sorted((ROOT / folder).glob("*.py")):
            files[str(path.relative_to(ROOT))] = path.read_bytes()
    for name in ("facct/__init__.py", "facct/requirements.txt", "facct/protocol/criteria.yaml",
                 "facct/conditional/config.json", "facct/consolidation/__init__.py",
                 "facct/consolidation/review_aggregates.py", "analysis/persona_common.py",
                 "analysis/build_dataset.py", "analysis/reliability.py"):
        files[name] = (ROOT / name).read_bytes()
    for folder in ("facct/outputs/tables", "facct/revision/outputs", "facct/conditional/outputs",
                   "facct/allocation/outputs", "facct/consolidation/outputs"):
        for path in sorted((ROOT / folder).glob("*.csv")):
            if safe_csv(path):
                files[str(path.relative_to(ROOT))] = path.read_bytes()
    for path in sorted((ROOT / "facct/paper/overleaf/tables").glob("*.tex")):
        files["paper_tables/" + path.name] = path.read_bytes()
    verification = ROOT / "facct/consolidation/verification/verification.json"
    result = json.loads(verification.read_text())
    assert result["status"] == "passed" and result["protected_unchanged"]
    summary = dict(status=result["status"], fresh_environment=result["fresh_environment"],
        runtime_seconds=result["runtime_seconds"],
        reproduced_files=sum(len(s["byte_identical_outputs"]) for s in result["stages"]),
        raw_data_included=False, redistribution_authorized=False,
        anonymity_certified=False, full_reanalysis_from_this_archive=False)
    files["LOCAL_VERIFICATION_SUMMARY.json"] = (json.dumps(summary, indent=2) + "\n").encode()
    files["README.md"] = b"""# Local code and aggregate review candidate

NOT A FULL DATA RELEASE. Author rights/anonymity approval is outstanding. Do not
upload this candidate on the basis of automated checks. It contains code, recorded
aggregate and item-ID numerical outputs, and generated paper tables. It excludes raw
prompt/response text, rater identities, private records, source manifests with named
files, original CHI documents, and Git history. Item IDs still require author review.

Using Python 3.12, run the dependency-free inspection command:

    python -m facct.consolidation.review_aggregates

This checks included file hashes and selected aggregate arithmetic. It does NOT
refit models or replicate bootstrap estimates. Test modules and analysis source are
included for inspection; tests requiring omitted inputs cannot run from this archive.
No claim of full reproducibility from this candidate is made.

Full local reproduction was separately completed from an isolated source snapshot
and newly installed pinned dependencies. Numerical CSV/figure outputs matched the
frozen originals byte for byte; see LOCAL_VERIFICATION_SUMMARY.json. In an authorized
complete checkout, the one-command reproduction entry point is:

    python -m facct.consolidation.verify --fresh-env

The complete checkout must supply original processed response/rating CSVs, source
domain CSVs, CHI reference outputs and snapshot, protocol/history, and Git metadata.
Those dependencies are deliberately NOT silently supplied in this candidate. Human
rights/consent review and an identity-safe data release are needed before claiming a
reviewer can reproduce every experiment. Code testing is not scientific validation,
publication clearance, or approval to redistribute corpus texts.

Paper mapping: original coverage/workload -> facct/outputs/tables/screening.csv;
fusion/cutoff/provenance -> facct/revision/outputs; trained increments ->
facct/conditional/outputs; common queues -> facct/allocation/outputs; reconstructed
text composition -> facct/consolidation/outputs. Main and held-out queues have
different quotas; their performance values are not interchangeable experiments.
"""
    for name, data in files.items():
        if IDENTITY.search(name) or IDENTITY.search(data.decode("utf-8")):
            raise ValueError(f"Potential identifying text in {name}; do not release")
    return files


def main():
    import hashlib
    files = payload()
    manifest = dict(scope="local code/aggregate candidate; no raw source text",
                    rights_approved=False, anonymity_certified=False,
                    files={name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())})
    files["ARTIFACT_MANIFEST.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 2, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    with tempfile.TemporaryDirectory(prefix="facct-candidate-check-") as directory:
        with zipfile.ZipFile(buffer) as archive:
            assert archive.testzip() is None
            assert all(not Path(n).is_absolute() and ".." not in Path(n).parts for n in archive.namelist())
            archive.extractall(directory)
        subprocess.run([sys.executable, "-m", "facct.consolidation.review_aggregates"],
                       cwd=directory, check=True)
    destination = ROOT / "facct/releases/PERSONA_FAccT_Code_Aggregates_REVIEW_CANDIDATE.zip"
    destination.write_bytes(buffer.getvalue())
    report = dict(file=destination.name, sha256=sha(destination), files=len(files),
                  extracted_archive_smoke_test="passed", raw_data_included=False,
                  author_release_approval="pending", anonymity_certified=False)
    (ROOT / "facct/consolidation/outputs/artifact_check.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
