"""
Baixa todos os arquivos da base.yaml em formato csv.

"""

import tempfile
import time
import zipfile
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml

destination_folder = "./data"

MAX_RETRIES = 5
CHUNK_SIZE = 1024 * 1024


def _stream_to_file(url: str, destination_path: Path) -> None:
    for attempt in range(1, MAX_RETRIES + 1):
        resume_from = destination_path.stat().st_size if destination_path.exists() else 0
        headers = {"Range": f"bytes={resume_from}-"} if resume_from else {}

        try:
            with requests.get(url, timeout=60, stream=True, headers=headers) as response:
                if resume_from and response.status_code != 206:
                    # servidor não suporta resume, recomeça do zero
                    resume_from = 0
                    destination_path.unlink(missing_ok=True)

                response.raise_for_status()

                mode = "ab" if resume_from else "wb"
                with open(destination_path, mode) as f:
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        f.write(chunk)
            return

        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError):
            if attempt == MAX_RETRIES:
                raise
            time.sleep(2 ** attempt)


def download_base(url: str, destination_folder: str = ".") -> None:
    destination = Path(destination_folder)
    destination.mkdir(parents=True, exist_ok=True)
    filename = Path(urlparse(url).path).name

    if ".csv" in url:
        _stream_to_file(url, destination / filename)

    elif ".zip" in url:
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = Path(tmp_dir) / filename
            _stream_to_file(url, zip_path)

            with zipfile.ZipFile(zip_path) as zip_file:
                for member in zip_file.namelist():
                    if member.lower().endswith(".csv"):
                        zip_file.extract(member, destination)

    else:
        raise ValueError("File extension not supported")


def main():
    with open('base.yaml', 'r') as f:
        base_definition = yaml.safe_load(f)

    contents = base_definition['content']
    for url in contents:
        print("Downloading {}".format(url))
        download_base(url, destination_folder=destination_folder)


if __name__ == '__main__':
    main()
