from pathlib import Path
from pypdf import PdfReader
import json
import openpyxl

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'references' / 'slides_text'
out.mkdir(parents=True, exist_ok=True)
index = []
for path in Path('E:/UsersData').glob('*.pdf'):
    if not ('Chuong ' in path.name or 'Chương ' in path.name):
        continue
    reader = PdfReader(str(path))
    pages = [p.extract_text() or '' for p in reader.pages]
    target = out / (path.stem + '.txt')
    target.write_text('\n\n'.join(f'=== TRANG {i+1} ===\n{t}' for i, t in enumerate(pages)), encoding='utf-8')
    index.append({'source': str(path), 'pages': len(pages), 'text': str(target.relative_to(ROOT))})
(out / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
registration = ROOT / 'Đăng kí nhóm - de tai - NNKHDL.xlsx'
if not registration.exists():
    registration = ROOT.parent / registration.name
wb = openpyxl.load_workbook(registration, data_only=True)
book = {s.title: list(s.values) for s in wb}
(ROOT / 'references' / 'registration.json').write_text(json.dumps(book, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
print(json.dumps(index, ensure_ascii=True, indent=2))
print('Registration sheets:', [(k, len(v)) for k,v in book.items()])
