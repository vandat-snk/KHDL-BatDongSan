"""Provenance and saved-artifact consistency, independent of document renderers."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

SOURCE_SHA256 = 'ef39f153f48a55af07baa86883cd9036652f6d52232fed0be6e8991c7a5bf811'
SOURCE_ROWS = 9004
CORE_CODE = ('src/pipeline.py', 'src/source_checks.py', 'src/artifact_contract.py')
DERIVATIVE_CODE = {
    'dashboard': ('tools/build_dashboard.py', 'src/dashboard_template.html'),
    'workbook': ('tools/build_workbook.mjs',),
}


def file_sha256(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def safe_relative(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ValueError(f'Artifact path outside project: {relative}')
    return candidate


def read_verified_source(raw: Path) -> tuple[list[dict], str]:
    if not raw.is_file():
        raise ValueError('Missing raw source. Run python scripts/download_data.py first.')
    actual = file_sha256(raw)
    if actual != SOURCE_SHA256:
        raise ValueError('Raw SHA-256 differs from the published source. No output was regenerated. '
                         'Keep the changed file for inspection; restore the verified source before retrying.')
    records = json.loads(raw.read_text(encoding='utf-8'))
    if not isinstance(records, list) or len(records) != SOURCE_ROWS:
        raise ValueError('Unexpected source schema or row count.')
    if any(not isinstance(row, dict) for row in records):
        raise ValueError('Every source record must be an object.')
    return records, actual


def validate_core_outputs(root: Path) -> dict:
    root = root.resolve()
    path = root / 'outputs/run_manifest.json'
    if not path.exists():
        raise ValueError('No verified run manifest. Run python src/pipeline.py first.')
    manifest = json.loads(path.read_text(encoding='utf-8'))
    if manifest.get('schema_version') != '2.0' or manifest.get('source_sha256') != SOURCE_SHA256:
        raise ValueError('Unsupported run manifest or unverified data source.')
    for kind in ('source_files', 'artifacts'):
        if not manifest.get(kind):
            raise ValueError(f'Empty manifest section: {kind}')
        for relative, expected in manifest[kind].items():
            artifact = safe_relative(root, relative)
            if not artifact.is_file() or file_sha256(artifact) != expected:
                raise ValueError(f'Stale or changed {relative}; rerun the pipeline before building or verifying outputs.')
    raw = root / 'data/raw/chotot_data.json'
    if raw.exists() and file_sha256(raw) != SOURCE_SHA256:
        raise ValueError('Local raw source was changed after the saved run.')
    analysis = json.loads((root / 'outputs/analysis.json').read_text(encoding='utf-8'))
    if analysis.get('run_id') != manifest['run_id']:
        raise ValueError('analysis.json belongs to another run.')
    return manifest


def register_derivative(root: Path, kind: str, target: Path) -> dict:
    manifest = validate_core_outputs(root)
    relative = target.resolve().relative_to(root.resolve()).as_posix()
    record = {'core_run_id': manifest['run_id'], 'path': relative,
              'sha256': file_sha256(target),
              'source_files': {name: file_sha256(root / name) for name in DERIVATIVE_CODE[kind]}}
    destination = root / f'outputs/{kind}_build.json'
    destination.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    return record


def validate_derivative(root: Path, kind: str, manifest: dict | None = None) -> dict:
    manifest = manifest or validate_core_outputs(root)
    metadata_path = root / f'outputs/{kind}_build.json'
    if not metadata_path.exists():
        raise ValueError(f'{kind} has no build record; recreate it from the current run.')
    metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
    if metadata.get('core_run_id') != manifest['run_id']:
        raise ValueError(f'{kind} belongs to an older pipeline run; recreate it.')
    target = safe_relative(root, metadata['path'])
    if not target.is_file() or file_sha256(target) != metadata['sha256']:
        raise ValueError(f'{kind} file changed or is missing.')
    for relative, expected in metadata.get('source_files', {}).items():
        if file_sha256(safe_relative(root, relative)) != expected:
            raise ValueError(f'{kind} generator changed; recreate the artifact.')
    if set(metadata.get('source_files', {})) != set(DERIVATIVE_CODE[kind]):
        raise ValueError(f'{kind} build record does not track all generator files.')
    return metadata
