"""
Pipeline completo: baixa os CSVs da ANP para uma pasta temporária (download.py)
e converte tudo para um único parquet (convert.py). Único artefato final: o parquet.

Rodar de dentro de `data/raw/diesel/`: `uv run main.py`.
"""

import tempfile
from pathlib import Path

import yaml

from convert import convert_to_parquet, read_csv
from download import download_base

base_yaml_path = "base.yaml"
output_path = "./data/diesel.parquet"


def main():
    with open(base_yaml_path, "r") as f:
        base_definition = yaml.safe_load(f)

    with tempfile.TemporaryDirectory() as tmp_dir:
        for url in base_definition["content"]:
            print(f"Baixando {url}")
            download_base(url, destination_folder=tmp_dir)

        csv_files = sorted(Path(tmp_dir).glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"Nenhum .csv baixado em {tmp_dir}")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        writer = None
        total_rows = 0
        try:
            for file_path in csv_files:
                print(f"Lendo {file_path.name}")
                df = read_csv(file_path)
                df["file_name"] = file_path.name
                total_rows += len(df)
                writer = convert_to_parquet(df, output_path, writer)
        finally:
            if writer is not None:
                writer.close()

    print(f"Total: {total_rows:,} linhas")
    print(f"Parquet salvo em {output_path}")


if __name__ == "__main__":
    main()
