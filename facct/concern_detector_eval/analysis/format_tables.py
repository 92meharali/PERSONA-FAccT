"""Typography-only normalization of numeric minus signs outside LaTeX math."""
import re
from pathlib import Path

for path in Path("paper/tables").glob("*.tex"):
    parts = re.split(r"(?<!\\)\$", path.read_text())
    for i in range(0,len(parts),2):
        parts[i]=re.sub(r"(?<![\w\\$-])-(?=\d)",lambda _:r"\ensuremath{-}",parts[i])
    path.write_text("$".join(parts))
