"""Audit the report structure, data provenance and Word/PDF export.

--visual-reviewed-pages records an actual manual PNG review; it does not perform
that review. Call only after inspecting the corresponding final rendered pages.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from lxml import etree
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
TARGET=DOCS/'BAO_CAO_TIEU_LUAN_6_CHUONG.docx'
PDF=TARGET.with_suffix('.pdf')
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--visual-reviewed-pages',default='')
    args=parser.parse_args()
    layout=json.loads((ROOT/'tmp/report_qa/word_layout.json').read_text(encoding='utf-8-sig'))
    pdf=PdfReader(PDF);assert len(pdf.pages)==layout['pages']
    text_pages=[page.extract_text() for page in pdf.pages]
    text='\n'.join(text_pages)
    for forbidden in ['Error! Reference source not found','Error! Bookmark not defined','Lỗi! Không xác định','[Nhóm bổ sung]','[[table:','[[figure:','\\frac','\\begin{','\\sum']:
        assert forbidden not in text,forbidden
    with ZipFile(TARGET) as archive:
        xml=etree.fromstring(archive.read('word/document.xml'))
        styles=etree.fromstring(archive.read('word/styles.xml'))
    doc=Document(TARGET)
    chapters=[p.text for p in doc.paragraphs if re.match(r'^Chương [1-6] ',p.text) and p.style.name=='Heading 1']
    assert len(chapters)==6
    assert len(xml.xpath('//m:oMath',namespaces=NS))==8==layout['native_equations']
    assert len(xml.xpath('//wp:inline',namespaces=NS))==9
    assert not xml.xpath('//w:pBdr',namespaces=NS) and not styles.xpath('//w:style[@w:styleId="Title"]//w:pBdr',namespaces=NS)
    captions=[p.text for p in doc.paragraphs if p.style.name=='Caption']
    figure_captions=[p for p in captions if p.startswith('Hình ')]
    table_captions=[p for p in captions if p.startswith('Bảng ')]
    assert [int(re.match(r'Hình (\d+):',p)[1]) for p in figure_captions]==list(range(1,10))
    assert [int(re.match(r'Bảng (\d+):',p)[1]) for p in table_captions]==list(range(1,21))
    assert len(doc.tables)==20
    for table in doc.tables:
        assert table.rows[0]._tr.find('.//'+f'{{{NS["w"]}}}tblHeader') is not None
    body=[];inside=False
    for p in doc.paragraphs:
        if p.style.name=='Heading 1' and p.text.startswith('Chương 1 '):inside=True
        if p.style.name=='Heading 1' and p.text=='Tài liệu tham khảo':inside=False
        if not inside or not p.text or p.style.name!='Normal':continue
        if p._p.xpath('.//m:oMath') or p._p.xpath('.//wp:inline'):continue
        if p.runs and all(run.font.name=='Consolas' for run in p.runs):continue
        assert p.alignment in (None,WD_ALIGN_PARAGRAPH.JUSTIFY),p.text[:80]
        body.append(p.text)
    for token in ['Nguyễn Ngọc Duy','Võ Văn Đạt','N23DCCN078','Nguyễn Thị Yến Nhi','N23DCCN112','Hứa Như Quỳnh','N23DCCN118','0,6484','0,7788','6.936','2,25']:
        assert token in text,token
    assert len(body)>60
    build=json.loads((DOCS/'report_src/build_manifest.json').read_text(encoding='utf-8'))
    source=ROOT/'docs/report_src/noi_dung.md'
    assert sha(source)==build['source_sha256']
    assert sha(ROOT/'outputs/analysis.json')==build['analysis_sha256']
    analysis=json.loads((ROOT/'outputs/analysis.json').read_text(encoding='utf-8'))
    assert build['core_run_id']==analysis['run_id']
    counts=analysis['counts'];assert counts['raw_count']==counts['clean_count']+counts['duplicate_count']+counts['rejected_count']
    for relative,digest in build['figure_assets_sha256'].items():assert sha(ROOT/relative)==digest
    reviewed=set(int(x) for x in args.visual_reviewed_pages.split(',') if x)
    assert reviewed==set(range(1,len(pdf.pages)+1)), 'Inspect every final page before recording completion'
    hashes={str(i):sha(ROOT/f'tmp/report_qa/pages/page-{i}.png') for i in sorted(reviewed)}
    result={'status':'passed','checked_at_utc':datetime.now(timezone.utc).isoformat(),
        'core_run_id':analysis['run_id'],'pages':len(pdf.pages),'chapters':chapters,'figures':9,'tables':20,'native_equations':8,
        'body_paragraphs_justified':len(body),'captions_and_bookmarks':'verified',
        'render_backend':layout['backend'],'page_rasterizer':'packaged render_docx.py with Word PDF adapter and Poppler',
        'visual_review':{'reviewer':'Codex inspection of final page PNGs','pages_reviewed':sorted(reviewed),'page_sha256':hashes,
                         'findings':'No clipping, missing math glyphs, overlapping captions, broken references or truncated table rows observed.'},
        'source_md_sha256':sha(source),'document_sha256':sha(TARGET),'pdf_sha256':sha(PDF),
        'builder_sha256':sha(ROOT/'tools/build_final_report.py'),
        'limitations_carried_into_report':['Historical convenience sample and heuristic labels; not verified transaction truth.',
             'Browser layout of latest dashboard and native Excel recalculation not claimed.',
             'No fresh installation on another machine; workbook authoring has an additional runtime dependency.',
             'SQL snapshot did not demonstrate a latency speedup.'],
        'old_drafts_modified_by_this_build':False}
    (DOCS/'report_src/QA_REPORT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    build['pre_word_export_document_sha256']=build.get('pre_word_export_document_sha256',build['document_sha256'])
    build['document_sha256']=result['document_sha256'];build['pdf_sha256']=result['pdf_sha256'];build['pages']=result['pages'];build['render_status']='rendered_and_visually_reviewed'
    (DOCS/'report_src/build_manifest.json').write_text(json.dumps(build,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='visual_review'},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
