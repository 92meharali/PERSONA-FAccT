# Verification completed on 10 October 2026

## Executed checks

- Full existing FAccT test suite plus the new independent-annotation tests:
  **90 passed**, 7.85 seconds in the isolated analysis environment.
- Main analysis: **2,000** paired prompt-cluster bootstrap replicates,
  **8.32 seconds** excluding environment setup.
- Second run in `/tmp/persona-annotation-reproduction`: **8.25 seconds**.
- Independent standard-library verifier reconstructed the majority labels,
  original policy selections and **112** original-policy target/budget cells.
- **Nine** numerical files were byte-identical across the two runs, including
  bootstrap intervals and agreement statistics.
- All **96** supplied source-file hashes and the protected repository input,
  configuration and manuscript hashes matched after execution.

Commands are in README.md; the executed main-run command and package versions are
recorded in outputs/manifest.json. Verification checks the implementation and
current records, not recruitment history, actual annotation dates, consent,
prospective ethics coverage or assessor independence.

## Scope of changes

Added the independent_annotation module, tests, analysis amendment, independent
verifier, generated outputs and this record. Updated facct/README.md,
facct/study/STATUS.md and facct/CHANGELOG.md to distinguish this follow-up from the
still-deferred practitioner sessions. Existing corpus data, annotation submissions,
prior computational outputs and the active manuscript were not edited. No GitHub
push, recruitment, new human judgments or manuscript integration was performed.

## Important interpretation

At 132/660 reviews, the reconstructed labels contain 19 positives in 13 prompts.
Original HumT catches 6, original normalized markers 12, original word length 4;
expected uniform random catches 3.8. HumT minus markers is -31.6 percentage points,
with an exploratory hypothetical-batch interval of -66.7 to +4.3 points. HumT minus
expected random is +11.6 points, with interval -6.7 to +30.0 points. These intervals
include zero and do not establish a robust ranking across new batches. The fixed
corpus counts themselves are exact conditional on the chosen mixed-version labels.

Do not replace original policies with the imported package's different queues;
those are explicitly retained as a separate sensitivity family. Do not describe
the A/B/C records as a completed, prospectively cleared external validation study
until the outstanding provenance documentation is checked. A/B versions differ,
and C assessed only disagreements. Agreement is not a validity guarantee.
