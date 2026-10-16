"""Reproduce paper-facing analyses from the packaged processed datasets.

Run from the supplement root:

    python3 -m analysis.run_from_processed

The raw-to-processed corpus build is intentionally excluded from the anonymous
review package. This runner regenerates reliability, descriptive, predictive,
domain-interaction, and sensitivity outputs from the supplied anonymous data.
"""

from __future__ import annotations

import time

from . import d_scope_audit, descriptives, domain_interactions, predictive, reliability


PHASES = [
    ("reliability", reliability.main),
    ("descriptives and construct relationships", descriptives.main),
    ("grouped cross-validation and ablations", predictive.main),
    ("domain interactions", domain_interactions.main),
    ("deception-risk sensitivity audit", d_scope_audit.main),
]


def main() -> None:
    started = time.time()
    for name, run in PHASES:
        phase_started = time.time()
        print(f"\n=== {name} ===")
        run()
        print(f"Completed in {time.time() - phase_started:.1f}s")
    print(f"\nAll packaged analyses completed in {time.time() - started:.1f}s")


if __name__ == "__main__":
    main()
