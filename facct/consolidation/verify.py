"""Rerun every analysis in an isolated copy, leaving all frozen outputs untouched."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

from .audit import ROOT, protected_hashes
from facct.analysis.validate_inputs import sha

STAGES = (("facct.analysis.run", "facct/outputs"),
          ("facct.revision.run", "facct/revision/outputs"),
          ("facct.conditional.run", "facct/conditional/outputs"),
          ("facct.allocation.run", "facct/allocation/outputs"))


def compare_outputs(expected, actual):
    paths = sorted(p for p in expected.rglob("*")
                   if p.is_file() and p.suffix in (".csv", ".pdf", ".png"))
    actual_names = {str(p.relative_to(actual)) for p in actual.rglob("*")
                    if p.is_file() and p.suffix in (".csv", ".pdf", ".png")}
    expected_names = {str(p.relative_to(expected)) for p in paths}
    if actual_names != expected_names:
        raise ValueError(f"Different output file sets: {actual_names ^ expected_names}")
    result = {}
    for path in paths:
        relative = str(path.relative_to(expected))
        if sha(path) != sha(actual / relative):
            raise ValueError(f"Nonidentical output: {expected.name}/{relative}")
        result[relative] = sha(path)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fresh-env", action="store_true",
                        help="Install pinned dependencies into a newly created environment")
    args = parser.parse_args()
    out = ROOT / "facct/consolidation/verification"
    out.mkdir(parents=True, exist_ok=True)
    before = protected_hashes()
    start = time.perf_counter()
    record = dict(status="running", fresh_environment=args.fresh_env, stages=[],
                  scientific_validation=False, source_revision=subprocess.check_output(
                      ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip())
    try:
        with tempfile.TemporaryDirectory(prefix="persona-facct-verify-") as temporary:
            work = Path(temporary) / "workspace"
            work.mkdir()
            for name in ("analysis", "data", "paper", "facct", "submission/chi2027_supplement"):
                shutil.copytree(ROOT / name, work / name, ignore=shutil.ignore_patterns(
                    "__pycache__", ".pytest_cache", "releases", "verification"))
            python = sys.executable
            if args.fresh_env:
                environment = Path(temporary) / "venv"
                subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True)
                python = str(environment / "bin/python")
                with (out / "install.log").open("w") as log:
                    subprocess.run([python, "-m", "pip", "install", "-r",
                                    str(work / "facct/requirements.txt")],
                                   stdout=log, stderr=subprocess.STDOUT, check=True)
            env = os.environ.copy()
            # The frozen programs read only the Git revision. Point them to the
            # original metadata without copying history into the scratch workspace.
            env["GIT_DIR"] = subprocess.check_output(
                ["git", "rev-parse", "--absolute-git-dir"], cwd=ROOT, text=True).strip()
            env["GIT_WORK_TREE"] = str(work)
            env["MPLCONFIGDIR"] = str(Path(temporary) / "matplotlib")
            record["environment"] = subprocess.check_output(
                [python, "-m", "pip", "freeze"], text=True).splitlines()
            for module, expected in STAGES:
                target = work / "facct/rerun" / module.split(".")[1]
                command = [python, "-m", module, "--output", str(target)]
                print(f"Reproducing {module} with 2,000 draws", flush=True)
                started = time.perf_counter()
                with (out / (module + ".log")).open("w") as log:
                    subprocess.run(command, cwd=work, env=env, stdout=log,
                                   stderr=subprocess.STDOUT, check=True)
                matched = compare_outputs(ROOT / expected, target)
                record["stages"].append(dict(module=module, runtime_seconds=time.perf_counter()-started,
                                             byte_identical_outputs=matched))
            with (out / "point_checks.log").open("w") as log:
                subprocess.run([python, "-m", "facct.analysis.verify_outputs"], cwd=work,
                               env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
            record["status"] = "passed"
    except Exception as exc:
        record["status"] = "failed"
        record["error"] = str(exc)
        raise
    finally:
        record["runtime_seconds"] = time.perf_counter() - start
        record["protected_files"] = len(before)
        record["protected_unchanged"] = before == protected_hashes()
        (out / "verification.json").write_text(json.dumps(record, indent=2) + "\n")
        if not record["protected_unchanged"]:
            raise RuntimeError("Protected originals changed")
    print(json.dumps({k: v for k, v in record.items() if k not in ("stages", "environment")}, indent=2))


if __name__ == "__main__":
    main()
