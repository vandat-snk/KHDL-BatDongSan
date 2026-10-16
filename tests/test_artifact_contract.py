"""Regression checks for wrong-source attribution and stale output detection."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / 'src/artifact_contract.py'
SPEC = importlib.util.spec_from_file_location('artifact_contract', MODULE)
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)
TEST_TMP = MODULE.parents[1] / 'tmp' / 'unit_tests'
TEST_TMP.mkdir(parents=True, exist_ok=True)


class ArtifactContractTests(unittest.TestCase):
    def fixture(self, root):
        (root/'outputs').mkdir()
        (root/'src').mkdir()
        (root/'src/pipeline.py').write_text('pipeline fixture', encoding='utf-8')
        (root/'outputs/analysis.json').write_text(json.dumps({'run_id':'test-run'}), encoding='utf-8')
        manifest={'schema_version':'2.0', 'run_id':'test-run', 'source_sha256':contract.SOURCE_SHA256,
                  'source_files':{'src/pipeline.py':contract.file_sha256(root/'src/pipeline.py')},
                  'artifacts':{'outputs/analysis.json':contract.file_sha256(root/'outputs/analysis.json')}}
        (root/'outputs/run_manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        return manifest

    def test_modified_raw_is_rejected_before_attribution(self):
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as directory:
            raw=Path(directory)/'custom.json';raw.write_text('[{"price":"fake"}]', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'SHA-256'):
                contract.read_verified_source(raw)

    def test_saved_output_and_source_edits_are_detected(self):
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as directory:
            root=Path(directory);self.fixture(root)
            self.assertEqual(contract.validate_core_outputs(root)['run_id'],'test-run')
            (root/'outputs/analysis.json').write_text('{"run_id":"another"}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Stale'):
                contract.validate_core_outputs(root)
            self.fixture_reset_analysis(root)
            (root/'src/pipeline.py').write_text('different code', encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Stale'):
                contract.validate_core_outputs(root)

    def fixture_reset_analysis(self, root):
        (root/'outputs/analysis.json').write_text(json.dumps({'run_id':'test-run'}), encoding='utf-8')

    def test_manifest_paths_cannot_escape_project(self):
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as directory:
            with self.assertRaisesRegex(ValueError,'outside'):
                contract.safe_relative(Path(directory), '../another-project/file.json')

    def test_old_derivative_run_is_not_accepted(self):
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as directory:
            root=Path(directory);self.fixture(root)
            (root/'outputs/dashboard_build.json').write_text(json.dumps({'core_run_id':'old-run'}),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'older'):
                contract.validate_derivative(root,'dashboard')

    def test_unverified_source_never_overwrites_existing_output(self):
        import sys
        sys.path.insert(0,str(MODULE.parent))
        from pipeline import main
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as directory:
            root=Path(directory)
            raw=root/'bad-source.json';raw.write_text('[]',encoding='utf-8')
            (root/'outputs').mkdir()
            saved=root/'outputs/analysis.json';saved.write_text('previous successful run',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'SHA-256'):
                main(['--raw',str(raw),'--output-root',str(root)])
            self.assertEqual(saved.read_text(encoding='utf-8'),'previous successful run')
            self.assertFalse((root/'data/processed').exists())

    def test_generation_failure_keeps_previous_published_files(self):
        import pipeline
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as directory:
            root=Path(directory);(root/'outputs').mkdir()
            saved=root/'outputs/analysis.json';saved.write_text('previous run',encoding='utf-8')
            def broken_generate(staging,*_):
                (staging/'outputs').mkdir()
                (staging/'outputs/analysis.json').write_text('unfinished new run',encoding='utf-8')
                raise RuntimeError('simulated chart failure')
            with patch.object(pipeline,'read_verified_source',return_value=([],contract.SOURCE_SHA256)), patch.object(pipeline,'generate_outputs',side_effect=broken_generate):
                with self.assertRaisesRegex(RuntimeError,'simulated'):
                    pipeline.main(['--output-root',str(root)])
            self.assertEqual(saved.read_text(encoding='utf-8'),'previous run')
            self.assertFalse((root/'outputs/run_manifest.json').exists())

if __name__=='__main__':
    unittest.main()
