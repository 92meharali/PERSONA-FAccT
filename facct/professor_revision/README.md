# Input-window and strict-cutoff checks

Reproduce with the repository environment:

```bash
.venv/bin/python -m facct.professor_revision.run
.venv/bin/python -m facct.professor_revision.build_assets
```

Runtime: about 16 seconds for all three domains and 2,000 paired prompt resamples
on this machine. Dependencies match `facct/requirements.txt`. The follow-up
comparison requires the authenticated private ID map at the location recorded in
the existing assessment manifest; missing or altered maps fail instead of being
replaced by an assumed row-order correspondence.

Read [protocol.md](protocol.md), [outputs/findings.md](outputs/findings.md) and
[the response to the professor](../submission/professor_response_2026-10-26.md).
The full performance CSV retains five deterministic rules plus expected random,
four budgets and every criterion/domain cell. Paired contrasts retain finite
bootstrap counts and sparse-support flags. Existing source files and original
results remain unchanged.

The [coding guide](coding_guide.md) describes the 61-case inspection. Full texts,
the assistant's draft codes and the review worksheet are under the ignored
`private/professor_revision_2026-10-26/` directory. Draft semantic frequencies
are not manuscript evidence. Author review is pending; the manuscript reports
only traceable original-label profiles for these cases.
