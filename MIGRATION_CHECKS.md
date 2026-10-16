# Migration Checks

Checked on 16 October 2026 in the new repository, using an isolated Python 3.12.14 environment and `facct/requirements.txt`.

- All 547 copied research files matched the source checkout byte-for-byte before migration.
- Snapshot hash verification passed.
- The research test suite passed: **93 tests**, 50.20 seconds.
- `python -m facct.analysis.verify_outputs` passed: **144 ranked operating points** checked against independent scikit-learn implementations. Source hashes, code hashes and saved output hashes were verified.
- A scan for common GitHub/OpenAI token and private-key patterns found no matches in the copied research files. This is a limited pattern check, not a comprehensive security audit.
- Private external follow-up returns and completed consent/eligibility records were not copied.

No full bootstrap rerun, raw follow-up reconstruction, new data collection, manuscript compilation or scientific validation was performed for this archive operation. Earlier recorded full-run checks remain historical evidence, clearly separated from this migration check.

The original CHI checkout and its remote were not modified.
