"""Rasterize the current Word-exported report with the bundled DOCX renderer.

Run render_final_report.ps1 first. --renderer can specify an installed Codex
render_docx.py explicitly; otherwise the latest installed skill is discovered.
"""
import argparse, importlib.util, json, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/BAO_CAO_TIEU_LUAN_DA_RA_SOAT.docx'
PDF=DOC.with_suffix('.pdf')
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--renderer',type=Path)
ap.add_argument('--output-dir',type=Path,default=ROOT/'tmp/report_qa/pages')
args=ap.parse_args()
if args.renderer is None:
    base=Path.home()/'.codex/plugins/cache/openai-primary-runtime/documents'
    choices=list(base.glob('*/skills/documents/render_docx.py'))
    if not choices:raise SystemExit('Supply the bundled document skill path with --renderer.')
    args.renderer=max(choices,key=lambda p:tuple(map(int,p.parents[2].name.split('.'))))
args.output_dir.mkdir(parents=True,exist_ok=True)
tempfile.tempdir=str(args.output_dir.resolve())
if not PDF.exists() or PDF.stat().st_mtime<DOC.stat().st_mtime:
    raise SystemExit('Export the current saved DOCX to PDF with render_final_report.ps1 first.')
spec=importlib.util.spec_from_file_location('packaged_renderer',args.renderer)
renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
def word_pdf(doc_path,user_profile,outdir,stem,verbose=False):
    if Path(doc_path).resolve()!=DOC.resolve():raise ValueError('Unexpected source document.')
    return str(PDF),'Microsoft Word export; packaged PDF rasterization.'
renderer.convert_to_pdf=word_pdf
pages=renderer.rasterize(str(DOC),str(args.output_dir.resolve()),120,False,False)
print(json.dumps({'pages':len(pages),'renderer':str(args.renderer),'output':str(args.output_dir)},ensure_ascii=False))
