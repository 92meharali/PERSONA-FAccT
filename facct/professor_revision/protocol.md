# Professor-requested sensitivity amendment, 26 October 2026

Written before this amendment's computation, after the earlier results and the
professor's feedback were inspected. This is exploratory analysis of an explored
corpus, not a preregistration. Original ratings, HumT scores, policy definitions,
results and the original three-comparison primary family remain frozen.

1. Reconstruct the unchanged full-text HumT, normalized-marker and length queues.
   Add normalized markers and length computed from exactly `response[:300]`,
   preserving the source scorer's character slicing (including partial tokens).
   Keep all responses and original scores. This matches the available scorer's
   length restriction on annotated text; it cannot authenticate historical scorer
   inputs. Transfer export/rated-text differences remain a separate limitation.
2. Retain all three domains and budgets 5%, 10%, 20%, 30%. Evaluate mean D >= 3,
   mean D > 3, mean D >= 4, mean F < 4 and mean OA < 4. D > 3 is not D >= 4:
   five-rater means between 3 and 4 are included. Where the existing follow-up
   ID map authenticates successfully, also evaluate its resolved MH labels.
3. Exact floor budgets and original seeded ID ties apply. Paired domain-specific
   prompt bootstrap: 2,000 draws, seed 20261026, re-ranking each resampled batch;
   all policies and criteria share each draw. Report pointwise 95% percentile
   intervals, finite draws, concern-bearing and nonconcern-bearing prompt counts.
   Compare H to full markers, H to prefix markers, prefix to full markers,
   and H to analytical expected random. No threshold or seed selection.
4. Enumerate every broad-D concern selected exclusively by H or full markers in
   the original MH queue. Expected counts from existing results: 20 and 41.
   Describe their original D levels, F/OA membership, condition, marker frequency,
   text length and existing follow-up membership. These are exact descriptive
   characteristics, not a new human assessment of meaning or severity.
5. Prepare a shuffled coding packet with prompt, response and neutral case ID;
   keep policy, score and label keys separate. A semantic coding exercise must
   identify its coder and evidence spans, distinguish assistant-generated
   interpretation from human coding, and preserve ambiguity. No invented
   independent coding, consensus, participant response, or reliability result.
6. Record input and output hashes, software versions, revision, command and
   elapsed runtime. Preserve original outputs; generate a separate report and
   manuscript tables for this amendment. Main conclusions must follow the checks,
   including any weakening of the original full-text comparison.
