"""Download and verify the exact public Mendeley dataset used in this project."""

from __future__ import annotations

import hashlib
import json
import pathlib
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
DATASET_ID = "5477zhnmn2"
VERSION = 2
FILE_ID = "aa75d051-79fa-4df0-9707-50382de9da4b"
EXPECTED_SHA256 = "ef39f153f48a55af07baa86883cd9036652f6d52232fed0be6e8991c7a5bf811"
DOWNLOAD_URL = (
    f"https://data.mendeley.com/public-files/datasets/{DATASET_ID}"
    f"/files/{FILE_ID}/file_downloaded"
)
METADATA_URL = f"https://data.mendeley.com/public-api/datasets/{DATASET_ID}/snapshot/{VERSION}"
MANIFEST_URL = (
    f"https://data.mendeley.com/public-api/datasets/{DATASET_ID}/files"
    f"?folder_id=root&version={VERSION}&$start=0&$limit=1000"
)


def checksum(path: pathlib.Path) -> str:
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def read_url(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "KHDL-Academic-Project/1.0",
            "Accept": "application/vnd.mendeley-public-dataset.1+json, application/json, */*",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    target = RAW / "chotot_data.json"
    if target.exists():
        actual = checksum(target)
        if actual != EXPECTED_SHA256:
            raise SystemExit(
                f"Existing raw file checksum differs: {actual}. "
                "Preserve it and inspect before downloading another copy."
            )
        print("Raw file already exists and matches the published SHA-256.")
    else:
        content = read_url(DOWNLOAD_URL)
        actual = hashlib.sha256(content).hexdigest()
        if actual != EXPECTED_SHA256:
            raise SystemExit(f"Download checksum differs: {actual}; raw file was not written.")
        json.loads(content.decode("utf-8"))
        target.write_bytes(content)
        print(f"Saved {len(content):,} verified bytes to {target}")

    for name, url in (
        ("mendeley_metadata.json", METADATA_URL),
        ("mendeley_file_manifest.json", MANIFEST_URL),
    ):
        destination = RAW / name
        if not destination.exists():
            content = read_url(url)
            json.loads(content.decode("utf-8-sig"))
            destination.write_bytes(content)

    rows = json.loads(target.read_text(encoding="utf-8"))
    print(f"Actual JSON records: {len(rows):,}; source description says 10,000.")
    print(f"SHA-256: {checksum(target)}")


if __name__ == "__main__":
    main()
