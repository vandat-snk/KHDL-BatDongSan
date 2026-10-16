"""Reproduce core artifacts and real test evidence; final report authoring is separate."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from artifact_contract import file_sha256,validate_core_outputs

def execute(script,*arguments):
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/script),*arguments],cwd=ROOT,check=True)

def run_tests():
    manifest=validate_core_outputs(ROOT)
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py')
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    record={'core_run_id':manifest['run_id'],'status':'passed' if result.wasSuccessful() else 'failed',
            'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
            'test_files':{p.relative_to(ROOT).as_posix():file_sha256(p) for p in sorted((ROOT/'tests').glob('test_*.py'))}}
    (ROOT/'outputs/python_test_results.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    if not result.wasSuccessful(): raise ValueError('Python tests failed; see output.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-download',action='store_true',help='Use existing verified raw file offline.')
    parser.add_argument('--skip-tests',action='store_true',help='Generate without claiming tests ran.')
    parser.add_argument('--workbook',action='store_true',help='Rebuild optional Excel; requires Node22+ and @oai/artifact-tool.')
    parser.add_argument('--node',default=shutil.which('node'),help='Path to Node.js for optional JS tests/workbook.')
    args=parser.parse_args()
    if not args.skip_download: execute(Path('scripts/download_data.py'))
    execute(Path('src/pipeline.py'))
    if args.workbook:
        if not args.node: raise ValueError('Node.js not found. Omit --workbook or provide --node.')
        subprocess.run([args.node,str(ROOT/'tools/build_workbook.mjs')],cwd=ROOT,check=True)
    execute(Path('tools/build_dashboard.py'))
    if not args.skip_tests:
        run_tests()
        if args.node: subprocess.run([args.node,str(ROOT/'tests/test_dashboard.mjs')],cwd=ROOT,check=True)
        else: print('JS tests not run: Node.js is optional and was not found.')
    execute(Path('scripts/demo_sql.py'))
    execute(Path('tools/verify_delivery.py'),'--require-workbook' if args.workbook else '--core-only')
    print('Core workflow finished. No final report generated; see audit and teacher requirement matrix.')

if __name__=='__main__':
    try: main()
    except (ValueError,subprocess.CalledProcessError) as exc:
        print('Project run FAILED: '+str(exc),file=sys.stderr);raise SystemExit(1)
