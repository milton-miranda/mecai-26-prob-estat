import duckdb

source_path = "../../raw/diesel/data/diesel.parquet"
output_path = "./diesel.parquet"

RENAME_SQL = f"""
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


def main():
    con = duckdb.connect()
    con.execute(f"copy ({RENAME_SQL}) to '{output_path}' (format parquet)")
    total_rows = con.execute(f"select count(*) from '{output_path}'").fetchone()[0]
    print(f"Total: {total_rows:,} linhas")
    print(f"Parquet salvo em {output_path}")


if __name__ == "__main__":
    main()
