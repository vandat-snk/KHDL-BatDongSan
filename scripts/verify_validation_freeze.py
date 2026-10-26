"""Verify frozen rules, sample IDs and AI review without reading evaluation text."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    path=ROOT/'docs/manual_validation/FREEZE_MANIFEST.json'
    data=json.loads(path.read_text())
    changed=[]
    for relative,expected in data['sha256'].items():
        file=ROOT/relative
        if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest()!=expected:changed.append(relative)
    if changed:raise SystemExit('Frozen files changed: '+', '.join(changed))
    print('PASS: frozen rules, sampling and development evidence match '+data['version'])
    print('No claim of human accuracy. Baseline outputs are still from the older code.')
if __name__=='__main__':main()
