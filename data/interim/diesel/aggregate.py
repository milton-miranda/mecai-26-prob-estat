import duckdb

source_path = "./diesel.parquet"
output_dir = "../../processed/diesel"

con = duckdb.connect()

AGGREGATIONS = {
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


def main():
    for name, sql in AGGREGATIONS.items():
        output_path = f"{output_dir}/{name}.parquet"
        con.execute(f"copy ({sql}) to '{output_path}' (format parquet)")
        total_rows = con.execute(f"select count(*) from '{output_path}'").fetchone()[0]
        print(f"{name}: {total_rows:,} linhas -> {output_path}")


if __name__ == "__main__":
    main()
