import io
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

data_folder = "./data"
output_path = "./data/diesel.parquet"

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


def read_csv(file_path: str) -> pd.DataFrame:

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


def convert_to_parquet(
    df: pd.DataFrame, destination: str, writer: pq.ParquetWriter | None
) -> pq.ParquetWriter:
    table = pa.Table.from_pandas(df, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter(destination, table.schema)
    writer.write_table(table)
    return writer


def main():
    csv_files = sorted(Path(data_folder).glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"Nenhum .csv encontrado em {data_folder}")

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
