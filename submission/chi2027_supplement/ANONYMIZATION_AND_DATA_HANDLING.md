# Anonymization and data handling

## Measures taken for anonymous review

- No author, institution, investigator, grant, annotator, repository, or
  committee names are included.
- Raters are represented only by functional pseudonyms such as
  `oa_annotator_1` and `anonymous_annotator_1`.
- The signed ethics approval and recruitment records are excluded because they
  contain identifying information.
- The generated run manifest has been replaced by a path-free environment
  description because the repository manifest records a local author path.
- Raw annotation files whose filenames contain rater names are excluded.

Model and source-dataset names are retained because they describe the study
materials and do not identify the authors.

## Stimulus text

The response-level dataset contains prompts and model responses needed to audit
the measurements. Some prompts resemble personal disclosures or contain
crisis, abuse, health, academic-integrity, and other sensitive scenarios. They
are research stimuli derived from the sources described in the paper, not
profiles of the annotators. Apparent names, email addresses, institutions, and
other identifiers appearing inside prompt or response text are part of the
stimulus content and must not be treated as author or annotator contact
information.

Some legacy stimulus exports contain visible character-encoding artifacts
(for example, mojibake punctuation or replacement characters). They are
retained verbatim so the review corpus matches the analysis input rather than
silently altering the research record. These artifacts do not denote missing
ratings.

## Review-use limitation

These materials are supplied for confidential peer review. They are not the
final public release and do not grant a reuse license. Redistribution and
downstream release remain subject to institutional review and the terms of the
source datasets. Authors should complete a source-by-source redistribution and
license check before publication.
