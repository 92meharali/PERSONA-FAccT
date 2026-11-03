"""Validate the compiled project and package only anonymous typesetting assets."""
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/"paper"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect(path, seen):
    if path in seen:
        return ""
    seen.add(path)
    source=path.read_text()
    expanded=source
    for name in re.findall(r"\\input\{([^}]+)\}",source):
        child=PAPER/(name if name.endswith(".tex") else name+".tex")
        assert child.exists(), f"Missing input {child}"
        expanded+="\n"+collect(child,seen)
    return expanded


def main():
    assets=set()
    source=collect(PAPER/"main.tex",assets)
    labels=re.findall(r"\\label\{([^}]+)\}",source)
    references=re.findall(r"\\(?:ref|pageref|autoref)\{([^}]+)\}",source)
    assert len(labels)==len(set(labels)), "Duplicate reference labels"
    assert not set(references)-set(labels), f"Unknown references {set(references)-set(labels)}"
    floats={l for l in labels if l.startswith(("fig:","tab:"))}
    assert not floats-set(references), f"Unreferenced floats {floats-set(references)}"
    bib=(PAPER/"references.bib").read_text()
    keys=re.findall(r"@\w+\s*\{\s*([^,]+),",bib)
    assert len(keys)==len(set(keys)), "Duplicate bibliography keys"
    citations={k.strip() for block in re.findall(r"\\cite\w*\{([^}]+)\}",source) for k in block.split(",")}
    assert not citations-set(keys), f"Unknown citations {citations-set(keys)}"
    for name in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}",source):
        f=PAPER/name
        assert f.exists(), f"Missing figure {name}"
        assets.add(f)
    for filename in ("acmart.cls","ACM-Reference-Format.bst","references.bib","README.md","AUTHOR_CHECKLIST.md","main.pdf"):
        assets.add(PAPER/filename)
    compile_inputs=[f for f in assets if f.suffix in (".tex",".bib",".cls",".bst") or f.parent.name=="figures"]
    assert max(f.stat().st_mtime for f in compile_inputs) <= (PAPER/"main.pdf").stat().st_mtime, "PDF is older than a compiled input"
    log=(PAPER/"main.log").read_text()
    assert not re.search(r"(?:Reference|Citation).*undefined|There were undefined|multiply defined|Overfull \\[hv]box",log), "Unresolved compile/layout diagnostics"
    pdf=PdfReader(PAPER/"main.pdf")
    pages=[page.extract_text() for page in pdf.pages]
    endmatter=next(i for i,p in enumerate(pages) if "Endmatter" in p and "Ethical Considerations Statement" in p)
    bibliography=next(i for i,p in enumerate(pages) if re.search(r"\nReferences\s*\n",p))
    appendix=next(i for i,p in enumerate(pages) if re.search(r"\nA\s+Corpus Details",p))
    assert endmatter<=14, f"Main text exceeds 14 pages: {endmatter}"
    assert bibliography-endmatter==1, "Endmatter not confined to one page"
    assert "Author confirmation required" not in "\n".join(pages), "Unresolved author placeholder"
    assert "Assessors were compensated through existing paid research roles." in source
    for private in ("92meharali","/Users/","Mehar Ali","private_study_id_map"):
        assert private not in source and private not in str(pdf.metadata), f"Identifying material: {private}"
    manifest=dict(revision="professor-feedback-2026-11-03",main_file="main.tex",main_text_pages=endmatter,
                  endmatter_pages=bibliography-endmatter,reference_pages=appendix-bibliography,
                  appendix_pages=len(pages)-appendix,total_pdf_pages=len(pages),
                  bibliography_entries=len(keys),cited_entries=len(citations),
                  unique_labels=len(labels),undefined_references=0,overfull_boxes=0,
                  status="compiled_author_final_checks_pending",
                  author_actions=["Verify historical Codex version information and any additional AI tools.",
                                  "Confirm final submission metadata, registration and approvals."],
                  files={str(f.relative_to(PAPER)):digest(f) for f in sorted(assets)})
    manifest_path=PAPER/"package_manifest.json"
    manifest_path.write_text(json.dumps(manifest,indent=2)+"\n")
    assets.add(manifest_path)
    release=ROOT/"releases"; release.mkdir(exist_ok=True)
    archive=release/"PERSONA_FAccT_Professor_Revision_2026-11-03.zip"
    with ZipFile(archive,"w",compression=ZIP_DEFLATED) as z:
        for f in sorted(assets): z.write(f,f.relative_to(PAPER))
    with ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(assets)
        assert not any("/Users/" in n or ".." in Path(n).parts for n in z.namelist())
    print(json.dumps({k:v for k,v in manifest.items() if k!="files"},indent=2))
    print("Archive:",archive)
    print("SHA256:",digest(archive))


if __name__=="__main__": main()
