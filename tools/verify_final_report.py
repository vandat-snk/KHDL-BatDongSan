"""Verify the current report. Manual review flags record an actual PNG inspection.

Default mode verifies the saved review, hashes and structure without rendering.
"""
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/BAO_CAO_TIEU_LUAN_DA_RA_SOAT.docx'
PDF=DOC.with_suffix('.pdf')
FOLDER=ROOT/'docs/review_20261029'
QA=FOLDER/'QA_REPORT.json'
sys.path.insert(0,str(ROOT/'src'))
from artifact_contract import validate_core_outputs
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)
def inspect():
    core=validate_core_outputs(ROOT)
    build=json.loads((FOLDER/'build.json').read_text(encoding='utf-8'))
    require(core['run_id']==build['core_run_id'],'Different report/core run IDs.')
    d=Document(DOC)
    chapters=[p.text for p in d.paragraphs if p.style.name=='Heading 1' and re.match(r'Chương [1-6] ',p.text)]
    require(len(chapters)==6,'Expected six chapters.')
    require(len(d.element.xpath('//m:oMath'))==8,'Expected eight native equations.')
    captions=[p for p in d.paragraphs if p.style.name=='Caption']
    figures=[p for p in captions if p.text.startswith('Hình ')]
    tables=[p for p in captions if p.text.startswith('Bảng ')]
    require([int(re.match(r'Hình (\d+):',p.text)[1]) for p in figures]==list(range(1,12)),'Invalid figure numbering.')
    require([int(re.match(r'Bảng (\d+):',p.text)[1]) for p in tables]==list(range(1,25)),'Invalid table numbering.')
    require(len(d.tables)==24,'Missing or uncaptioned table.')
    for p in tables:require(p._p.getnext().tag.endswith('}tbl'),'Table separated from caption.')
    for p in figures:require(bool(p._p.getprevious().xpath('.//w:drawing')),'Image separated from caption.')
    for t in d.tables:require(bool(t.rows[0]._tr.xpath('./w:trPr/w:tblHeader')),'Table header not repeated.')
    bookmarks=set(d.element.xpath('//w:bookmarkStart/@w:name'))
    for field in d.element.xpath('//w:fldSimple/@w:instr'):
        if 'PAGEREF' in field:require(field.split()[1] in bookmarks,'Broken page reference.')
    text='\n'.join(p.text for p in d.paragraphs)
    for bad in ['slide','giáo trình','trang PDF','DOI_CHIEU_SLIDE',r'\frac',r'\begin{']:
        require(bad.casefold() not in text.casefold(),'Forbidden content: '+bad)
    refs=[p for p in d.paragraphs if re.match(r'^\[\d+\]',p.text)]
    require([int(re.match(r'\[(\d+)\]',p.text)[1]) for p in refs]==list(range(1,12)),'Invalid reference numbering.')
    pdf=PdfReader(PDF);pdftext='\n'.join(p.extract_text() for p in pdf.pages)
    for bad in ['Error! Reference source not found','Error! Bookmark not defined','Lỗi! Không xác định','[[figure:','[[table:']:
        require(bad not in pdftext,'Broken PDF field: '+bad)
    for token in ['6.911','6.652','2,25','32,50','43/58','8/8','0,1833','Nguyễn Ngọc Duy','N23DCCN078','N23DCCN112','N23DCCN118']:
        require(token in pdftext,'Missing report token: '+token)
    active=False;count=0
    for p in d.paragraphs:
        if p.style.name=='Heading 1' and p.text.startswith('Chương 1 '):active=True
        if p.style.name=='Heading 1' and p.text=='Tài liệu tham khảo':active=False
        if not active or not p.text or p.style.name!='Normal':continue
        if p._p.xpath('.//m:oMath|.//w:drawing'):continue
        if p.runs and all(r.font.name=='Consolas' for r in p.runs):continue
        alignment=p.alignment
        style=p.style
        while alignment is None and style is not None:
            alignment=style.paragraph_format.alignment
            style=style.base_style
        require(alignment==WD_ALIGN_PARAGRAPH.JUSTIFY,'Body not justified: '+p.text[:60]);count+=1
    return {'core_run_id':core['run_id'],'pages':len(pdf.pages),'chapters':chapters,
            'figures':11,'tables':24,'native_equations':8,'justified_body_paragraphs':count,
            'artifacts':{p.relative_to(ROOT).as_posix():sha(p) for p in [DOC,PDF,DOC.with_suffix('.md')]},
            'analysis_commit':build['analysis_commit'],'analysis_sha256':sha(ROOT/'outputs/analysis.json'),
            'extended_results_sha256':sha(ROOT/'outputs/extended/results.json')}
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--visual-reviewed-pages',default='')
    ap.add_argument('--page-dir',type=Path,default=ROOT/'tmp/report_qa/pages')
    args=ap.parse_args();record=inspect()
    if args.visual_reviewed_pages:
        pages=set(map(int,args.visual_reviewed_pages.split(',')))
        require(pages==set(range(1,record['pages']+1)),'Inspect every final PNG before recording completion.')
        record.update(status='passed',checked_at_utc=datetime.now(timezone.utc).isoformat(),
            visual_review={'reviewer':'Codex inspection of final page PNGs','pages_reviewed':sorted(pages),
            'page_sha256':{str(i):sha(args.page_dir/f'page-{i}.png') for i in sorted(pages)},
            'findings':'No clipping, missing math glyphs, broken references or overlapping captions observed.'},
            limitations=['No independent human-label validation claimed.',
                         'Native browser layout and Microsoft Excel UI acceptance not claimed.',
                         'Original private annotation XLSX absent from public repository.',
                         'SQL timing is one sequential warm-cache illustration.'])
        QA.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
        metadata={key:record[key] for key in ['core_run_id','pages','artifacts','extended_results_sha256']}
        metadata.update(visual_review='All final Word-rendered pages inspected as PNGs.',qa_record='docs/review_20261029/QA_REPORT.json')
        (ROOT/'outputs/report_build.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    else:
        saved=json.loads(QA.read_text(encoding='utf-8'))
        for key in ['core_run_id','pages','artifacts','analysis_sha256','extended_results_sha256']:
            require(saved[key]==record[key],'Changed after visual review: '+key)
        require(saved['status']=='passed' and len(saved['visual_review']['pages_reviewed'])==record['pages'],'Incomplete recorded visual review.')
        record.update(status='saved_hashes_and_structure_verified',visual_review='Recorded inspection matches these DOCX/PDF hashes. No new visual inspection inferred.')
    display={k:v for k,v in record.items() if k!='visual_review'}
    display['visual_review']='Complete inspection recorded for the same final artifacts; see QA_REPORT.json.'
    print(json.dumps(display,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
