"""Use the packaged DOCX renderer with Word's PDF on Windows without LibreOffice.

render_final_report.ps1 must first update/save the DOCX and export its PDF. The
packaged renderer still performs its normal Poppler rasterization to page PNGs.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import tempfile

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'tmp/report_qa'
SKILL=Path('C:/Users/thanh/.codex/plugins/cache/openai-primary-runtime/documents/26.1013.11914/skills/documents/render_docx.py')
DOC=ROOT/'docs/BAO_CAO_TIEU_LUAN_6_CHUONG.docx'
PDF=DOC.with_suffix('.pdf')
layout=json.loads((QA/'word_layout.json').read_text(encoding='utf-8-sig'))
assert PDF.is_file() and PDF.stat().st_mtime >= DOC.stat().st_mtime
assert layout['backend'].startswith('Microsoft Word')
temp=QA/'renderer_temp';temp.mkdir(parents=True,exist_ok=True)
tempfile.tempdir=str(temp)
spec=importlib.util.spec_from_file_location('packaged_docx_renderer',SKILL)
renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)


def use_word_pdf(doc_path,user_profile,outdir,stem,verbose=False):
    assert Path(doc_path).resolve()==DOC.resolve()
    return str(PDF),'Windows backend: Microsoft Word export; LibreOffice unavailable.'


renderer.convert_to_pdf=use_word_pdf
paths=renderer.rasterize(str(DOC),str(QA/'pages'),144,False,False)
assert len(paths)==layout['pages']
print(json.dumps({'backend':layout['backend'],'rasterizer':str(SKILL),'pages':len(paths),'output':str(QA/'pages')},ensure_ascii=False))
