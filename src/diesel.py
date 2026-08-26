"""
Ingestão, limpeza e agregação dos dados de preço de diesel (ANP).

Pipeline: data/raw/diesel/base.yaml
    -> download_all()      baixa os csv/zip da ANP para data/raw/diesel/data/
    -> convert_to_parquet() concatena os csv em data/raw/diesel/data/diesel.parquet
    -> clean()               filtra produtos diesel e renomeia colunas em
                              data/interim/diesel/diesel.parquet
    -> aggregate()            gera as bases agregadas em data/processed/diesel/
"""

import io
import tempfile
import time
import zipfile
from pathlib import Path
from urllib.parse import urlparse

import duckdb
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests
import yaml

from src.config import DATA_INTERIM, DATA_PROCESSED, DATA_RAW

RAW_DIR = DATA_RAW / "diesel"
BASE_YAML_PATH = RAW_DIR / "base.yaml"
RAW_CSV_DIR = RAW_DIR / "data"
RAW_PARQUET_PATH = RAW_CSV_DIR / "diesel.parquet"
INTERIM_PARQUET_PATH = DATA_INTERIM / "diesel" / "diesel.parquet"
PROCESSED_DIR = DATA_PROCESSED / "diesel"

MAX_RETRIES = 5
CHUNK_SIZE = 1024 * 1024

TEXT_COLUMNS = [
    "Regiao - Sigla",
    "Estado - Sigla",
    "Municipio",
    "Revenda",
    "CNPJ da Revenda",
    "Nome da Rua",
    "Numero Rua",
    "Complemento",
    "Bairro",
    "Cep",
    "Produto",
    "Unidade de Medida",
    "Bandeira",
]


# --- download -----------------------------------------------------------


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
            time.sleep(2**attempt)


def download_base(url: str, destination_folder: Path) -> None:
    destination_folder.mkdir(parents=True, exist_ok=True)
    filename = Path(urlparse(url).path).name

    if ".csv" in url:
        _stream_to_file(url, destination_folder / filename)

    elif ".zip" in url:
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = Path(tmp_dir) / filename
            _stream_to_file(url, zip_path)

            with zipfile.ZipFile(zip_path) as zip_file:
                for member in zip_file.namelist():
                    if member.lower().endswith(".csv"):
                        zip_file.extract(member, destination_folder)

    else:
        raise ValueError("File extension not supported")


def download_all(
    base_yaml_path: Path = BASE_YAML_PATH, destination_folder: Path = RAW_CSV_DIR
) -> None:
    with open(base_yaml_path, "r") as f:
        base_definition = yaml.safe_load(f)

    for url in base_definition["content"]:
        print(f"Baixando {url}")
        download_base(url, destination_folder=destination_folder)


# --- convert (csv -> parquet) --------------------------------------------


def read_csv(file_path: Path) -> pd.DataFrame:
    with open(file_path, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1252")

    return pd.read_csv(
        io.StringIO(text),
        sep=";",
        decimal=",",
        dtype={column: "string" for column in TEXT_COLUMNS},
        parse_dates=["Data da Coleta"],
        dayfirst=True,
    )


def _write_parquet_chunk(
    df: pd.DataFrame, destination: Path, writer: pq.ParquetWriter | None
) -> pq.ParquetWriter:
    table = pa.Table.from_pandas(df, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter(destination, table.schema)
    writer.write_table(table)
    return writer


def convert_to_parquet(csv_dir: Path = RAW_CSV_DIR, output_path: Path = RAW_PARQUET_PATH) -> None:
    csv_files = sorted(Path(csv_dir).glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"Nenhum .csv encontrado em {csv_dir}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    writer = None
    total_rows = 0
    try:
        for file_path in csv_files:
            print(f"Lendo {file_path.name}")
            df = read_csv(file_path)
            df["file_name"] = file_path.name
            total_rows += len(df)
            writer = _write_parquet_chunk(df, output_path, writer)
    finally:
        if writer is not None:
            writer.close()

    print(f"Total: {total_rows:,} linhas")
    print(f"Parquet salvo em {output_path}")


# --- clean (filtra diesel + renomeia colunas) -----------------------------


def clean(source_path: Path = RAW_PARQUET_PATH, output_path: Path = INTERIM_PARQUET_PATH) -> None:
    rename_sql = f"""
        select
            "Regiao - Sigla" as regiao_sigla,
            "Estado - Sigla" as estado_sigla,
            "Municipio" as municipio,
            "Revenda" as revenda,
            "CNPJ da Revenda" as cnpj_da_revenda,
            "Nome da Rua" as nome_da_rua,
            "Numero Rua" as numero_da_rua,
            "Complemento" as complemento,
            "Bairro" as bairro,
            "Cep" as cep,
            "Produto" as produto,
            "Data da Coleta" as data_da_coleta,
            "Valor de Venda" as valor_de_venda,
            "Valor de Compra" as valor_de_compra,
            "Unidade de Medida" as unidade_de_medida,
            "Bandeira" as bandeira,
            "file_name" as file_name
        from '{source_path}'
        where upper("Produto") like '%DIESEL%'
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute(f"copy ({rename_sql}) to '{output_path}' (format parquet)")
    total_rows = con.execute(f"select count(*) from '{output_path}'").fetchone()[0]
    print(f"Total: {total_rows:,} linhas")
    print(f"Parquet salvo em {output_path}")


# --- aggregate (bases mensais/anuais para análise) -------------------------


def _aggregations(source_path: Path) -> dict[str, str]:
    return {
        "mensal_geral": f"""
            select
                date_trunc('month', data_da_coleta) as mes,
                avg(valor_de_venda) as preco_medio,
                median(valor_de_venda) as preco_mediano,
                stddev(valor_de_venda) as desvio_padrao,
                count(*) as n
            from '{source_path}'
            group by 1
            order by 1
        """,
        "mensal_estado": f"""
            select
                date_trunc('month', data_da_coleta) as mes,
                estado_sigla,
                avg(valor_de_venda) as preco_medio,
                median(valor_de_venda) as preco_mediano,
                stddev(valor_de_venda) as desvio_padrao,
                count(*) as n
            from '{source_path}'
            group by 1, 2
            order by 1, 2
        """,
        "mensal_regiao": f"""
            select
                date_trunc('month', data_da_coleta) as mes,
                regiao_sigla,
                avg(valor_de_venda) as preco_medio,
                median(valor_de_venda) as preco_mediano,
                stddev(valor_de_venda) as desvio_padrao,
                count(*) as n
            from '{source_path}'
            group by 1, 2
            order by 1, 2
        """,
        "variacao_anual": f"""
            with anual as (
                select
                    year(data_da_coleta) as ano,
                    avg(valor_de_venda) as preco_medio,
                    count(*) as n
                from '{source_path}'
                group by 1
            )
            select
                ano,
                preco_medio,
                n,
                round(
                    (preco_medio - lag(preco_medio) over (order by ano))
                    / lag(preco_medio) over (order by ano) * 100,
                    2
                ) as variacao_yoy_pct
            from anual
            order by ano
        """,
    }


def aggregate(source_path: Path = INTERIM_PARQUET_PATH, output_dir: Path = PROCESSED_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    for name, sql in _aggregations(source_path).items():
        output_path = output_dir / f"{name}.parquet"
        con.execute(f"copy ({sql}) to '{output_path}' (format parquet)")
        total_rows = con.execute(f"select count(*) from '{output_path}'").fetchone()[0]
        print(f"{name}: {total_rows:,} linhas -> {output_path}")


if __name__ == "__main__":
    download_all()
    convert_to_parquet()
    clean()
    aggregate()
