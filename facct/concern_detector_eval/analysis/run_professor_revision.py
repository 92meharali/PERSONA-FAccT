"""Reproduce the cached-score revision, tables and figures without API calls."""
import argparse
import subprocess
import sys

p=argparse.ArgumentParser(description=__doc__)
p.add_argument("--repo",required=True)
p.add_argument("--study",required=True)
a=p.parse_args()
commands=[
    ["-m","analysis.followup_semantic","--repo",a.repo,"--study",a.study],
    ["-m","analysis.revision_reporting","--repo",a.repo],
    ["-m","analysis.make_alignment_figure"],
    ["-m","analysis.format_tables"],
    ["-m","pytest","-q"],
]
for command in commands:
    subprocess.run([sys.executable,*command],check=True)
