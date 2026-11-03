"""Reproducible analyses supporting the revision of the HumT screening paper.

Modules
-------
common            shared IO, Wilson intervals, matched-queue-size flagging
paired_detection  exact McNemar, cluster bootstrap, Bayesian posterior, power
llm_judge         pinned, cached LLM-judge comparator (semantic baseline)
semantic_screen   embedding-similarity screening comparator (semantic baseline)
cue_overlap       rubric-cue leakage audit for the marker baseline
score_audit       historical-vs-rescored HumT authentication
"""
