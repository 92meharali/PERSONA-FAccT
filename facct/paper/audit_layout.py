"""Measure rendered section boundaries; never substitute a word-count estimate."""
import argparse
import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def audit(pdf, source, output, inspection=None, date="2026-10-24"):
    reader = PdfReader(pdf)
    pages = [p.extract_text() or "" for p in reader.pages]

    def first(pattern, start=0):
        found = [i + 1 for i, page in enumerate(pages) if i >= start and re.search(pattern, page, re.M)]
        if not found:
            raise ValueError(f"Cannot identify rendered section boundary: {pattern}")
        return found[0]

    endmatter = first(r"^\s*Endmatter\s*$")
    references = first(r"^\s*References\s*$", endmatter)
    appendix = first(r"^\s*A\s+Label Agreement and Cutoff Diagnostics\s*$", references)
    record = {
        "date": date, "pdf_sha256": sha(pdf), "source_sha256": sha(source),
        "bibliography_sha256": sha(Path(source).with_name("references.bib")),
        "class_sha256": sha(Path(source).with_name("acmart.cls")),
        "engine": "pdfLaTeX via isolated TinyTeX 2026.10", "total_pages": len(pages),
        "main_content_pages": endmatter-1,
        "endmatter_pages": references-endmatter,
        "reference_pages": appendix-references,
        "appendix_pages": len(pages)-appendix+1,
        "endmatter_starts": endmatter, "references_start": references,
        "appendix_starts": appendix,
        "main_limit": 14, "endmatter_limit": 1,
        "within_main_limit": endmatter-1 <= 14,
        "within_endmatter_limit": references-endmatter <= 1,
        "visual_inspection": inspection or "pending",
        "guideline": "https://facctconference.org/2027/authorguide.html",
        "note": "Counts apply to this rendered PDF; author/ethics/overlap eligibility is not certified.",
    }
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2) + "\n")
    for i, page in enumerate(pages, 1):
        lines = [line for line in page.splitlines() if line.strip() and not line.strip().isdigit()]
        print(f"Page {i}: {' | '.join(lines[:4])[:220]}")
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--inspection", help="Record completed manual visual checks, not inferred approval")
    parser.add_argument("--date", default="2026-10-24", help="Date of this rendering audit")
    args = parser.parse_args()
    audit(args.pdf, args.source, args.output, args.inspection, args.date)
