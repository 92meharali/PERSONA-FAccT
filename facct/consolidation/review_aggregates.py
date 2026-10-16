"""Standard-library checks possible without redistribution of response text."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(relative):
    with (ROOT / relative).open() as stream:
        return list(csv.DictReader(stream))


def main():
    manifest = ROOT / "ARTIFACT_MANIFEST.json"
    if manifest.exists():
        entries = json.loads(manifest.read_text())["files"]
        for name, expected in entries.items():
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    table = read("facct/outputs/tables/screening.csv")
    points = [r for r in table if r["policy"] == "high_H" and
              float(r["budget"]) == .2 and r["domain"] != "pooled"]
    assert len(points) == 9
    for row in points:
        n, k, p, caught = (float(row[c]) for c in ("n", "selected", "concerns", "caught"))
        assert k == int(n * .2)
        assert caught + float(row["missed"]) == p
        assert abs(caught / p - float(row["recall"])) < 1e-12
        assert abs(caught / k - float(row["precision"])) < 1e-12
    increments = [r for r in read("facct/conditional/outputs/conditional_lift.csv")
                  if float(r["budget"]) == .2]
    assert len(increments) == 9
    assert all(float(r["lo"]) <= 0 <= float(r["hi"]) for r in increments)
    print(json.dumps(dict(status="passed", high_H_reference_cells=len(points),
        incremental_cells=len(increments), raw_data_reanalysis=False,
        scope="archive hashes and arithmetic consistency only; not statistical replication"), indent=2))


if __name__ == "__main__":
    main()
