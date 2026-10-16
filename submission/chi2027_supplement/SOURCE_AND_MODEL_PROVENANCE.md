# Source-dataset and model provenance

The packaged corpus combines adapted natural prompts with study-authored
adversarial prompts. This document records the third-party sources needed to
interpret the corpus; it does not supersede their licenses or terms.

## Prompt sources

| Domain | Natural-prompt source | Reference |
|---|---|---|
| Mental health | CounselBench-Eval | Li et al., *CounselBench: A Large-Scale Expert Evaluation and Adversarial Benchmarking of Large Language Models in Mental Health Question Answering*, arXiv:2506.08584 |
| Education | Bridge | Wang et al., *Bridging the Novice--Expert Gap via Models of Decision-Making*, NAACL 2024, https://doi.org/10.18653/v1/2024.naacl-long.120 |
| Education | MathDial | Macina et al., *MathDial*, EMNLP Findings 2023, https://doi.org/10.18653/v1/2023.findings-emnlp.372 |
| General health | HealthBench | Arora et al., *HealthBench*, arXiv:2505.08775, https://doi.org/10.48550/arXiv.2505.08775 |

The natural prompts were selected or adapted for single-turn evaluation.
Study-authored adversarial prompts probe domain-specific boundary, safety,
authority, dependency, and anthropomorphism failures. The `condition` column
distinguishes natural and adversarial items.

## Response generation

The analyzed corpus contains responses from three model families:

- `gpt-5.6-sol`, accessed through the OpenAI Responses API;
- `anthropic/claude-opus-4.8`, accessed through the OpenRouter Chat
  Completions API; and
- `z-ai/glm-5.2`, accessed through the OpenRouter Chat Completions API.

The normalized analysis labels are `gpt_5_6`, `claude_opus_4_8`, and `glm`.
Model identity was hidden from annotators. API-hosted models may change or
become unavailable, so exact response regeneration is not guaranteed; the
generated responses used in the reported analysis are preserved in
`analysis/processed/persona_all.csv`.

## Human-likeness measurement

`H` was computed with the HumT approach:

Cheng, Yu, and Jurafsky, *HumT DumT: Measuring and Controlling Human-Like
Language in LLMs*, ACL 2025,
https://doi.org/10.18653/v1/2025.acl-long.1261.

## Redistribution status

This anonymous package is supplied for confidential review. Before a public
release, the authors must verify the licenses and redistribution conditions for
each upstream source and add the required attribution and license notices. No
upstream source license is replaced or expanded by this package.
