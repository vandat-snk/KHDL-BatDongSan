"""Exercise a disposable source-only copy without the original outputs or environment.

Uses the invoking Python with already installed requirements; it does not claim a
new OS or fresh pip install was tested. Source download is checked separately.
"""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from artifact_contract import read_verified_source


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--node',help='Optional Node executable for dashboard JS checks.')
    args=parser.parse_args()
    read_verified_source(ROOT/'data/raw/chotot_data.json')
    log_dir=ROOT/'tmp/portability_checks';log_dir.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='source_copy_',dir=log_dir) as temporary:
        copy=Path(temporary)
        for folder in ('src','scripts','tools','tests','docs','references'):
            for path in (ROOT/folder).rglob('*'):
                if path.is_file() and path.suffix in ('.py','.mjs','.html','.md') and '__pycache__' not in path.parts and 'slides_text' not in path.parts:
                    target=copy/path.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target)
        for filename in ('requirements.txt','README.md'):
            shutil.copy2(ROOT/filename,copy/filename)
        # First reproduce a new clone's missing-raw condition without touching the original.
        missing=subprocess.run([sys.executable,'-X','utf8','src/pipeline.py'],cwd=copy,capture_output=True,text=True,encoding='utf-8')
        (log_dir/'missing_source.log').write_text(missing.stdout+missing.stderr,encoding='utf-8')
        if missing.returncode==0 or 'Missing raw source' not in missing.stderr or (copy/'outputs').exists():
            raise ValueError('Missing-source behavior was not safe/actionable.')
        raw=copy/'data/raw';raw.mkdir(parents=True)
        shutil.copy2(ROOT/'data/raw/chotot_data.json',raw/'chotot_data.json')
        command=[sys.executable,'-X','utf8','scripts/run_project.py','--skip-download']
        if args.node: command+=['--node',args.node]
        process=subprocess.run(command,cwd=copy,capture_output=True,text=True,encoding='utf-8')
        (log_dir/'source_copy_run.log').write_text(process.stdout+process.stderr,encoding='utf-8')
        if process.returncode: raise ValueError('Source-copy run failed; inspect tmp/portability_checks/source_copy_run.log')
        original=json.loads((ROOT/'data/processed/listings_clean.json').read_text(encoding='utf-8'))
        repeated=json.loads((copy/'data/processed/listings_clean.json').read_text(encoding='utf-8'))
        if original!=repeated: raise ValueError('Source-copy cleaned data/labels differ from original run.')
        audit=json.loads((copy/'outputs/AUDIT_RESULTS.json').read_text(encoding='utf-8'))
        result={'status':'passed','scope':'Source-only disposable copy using the same installed Python and requirements; no .venv, node_modules, old outputs or temporary PDF copied.',
                'original_run_id':json.loads((ROOT/'outputs/run_manifest.json').read_text(encoding='utf-8'))['run_id'],
                'copied_run_id':audit['core_run_id'],'missing_source_rejected_before_outputs':True,
                'cleaned_records_identical':len(repeated),'python_tests':audit['python_tests'],
                'dashboard_tests':audit['dashboard_tests']['status'],
                'not_tested':['Fresh pip installation','Download on another network','Excel authoring outside Codex runtime','Another operating system']}
        (ROOT/'outputs/portability_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(result,ensure_ascii=True,indent=2))


if __name__=='__main__': main()
