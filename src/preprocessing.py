import pandas as pd
import numpy as np
from pathlib import Path
from huggingface_hub import hf_hub_download

def padronizar_texto(coluna_pandas):
    """Remove acentos, espaços e deixa o texto em caixa baixa."""
    return (
        coluna_pandas.astype(str)
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

def consolidar_base_econometrica(salvar_parquet: bool = True) -> pd.DataFrame:
    """
    Carrega os 4 datasets pré-processados (Preço, Safra, Diesel, Bolsa Família),
    alinha as chaves temporais e geograficas, executa o merge baseado na tabela 
    de preços do feijão e exporta a planilha final consolidada.
    """
    
    # Caminhos
    c_diesel = hf_hub_download(repo_id="pbf-feijao-mecai-usp/bf-feijao-dados", filename="interim/diesel/diesel_deflacionado.parquet", repo_type="dataset")
    c_safra = hf_hub_download(repo_id="pbf-feijao-mecai-usp/bf-feijao-dados", filename="interim/safra/producao_feijao_tons.parquet", repo_type="dataset")
    c_precos = hf_hub_download(repo_id="pbf-feijao-mecai-usp/bf-feijao-dados", filename="raw/painel_feijao_deflacionado.csv", repo_type="dataset")
    c_repasse = hf_hub_download(repo_id="pbf-feijao-mecai-usp/bf-feijao-dados", filename="raw/Painel_Unificado_2004_2026_Deflacionado.xlsx", repo_type="dataset")

    df_diesel = pd.read_parquet(c_diesel)
    df_safra = pd.read_parquet(c_safra)
    df_precos = pd.read_csv(c_precos)
    df_repasse = pd.read_excel(c_repasse)

    # Alinhando as datas
    
    print("Alinhando as datas")
    
    # 1. Base Preços
    df_precos["data_referencia"] = pd.to_datetime(df_precos["ano"].astype(str) + "-" + df_precos["mes"].astype(str) + "-01")
    df_precos['capital_join'] = padronizar_texto(df_precos['capital'])
    
    # 2. Base Bolsa Família
    df_repasse["data_referencia"] = pd.to_datetime(df_repasse["periodo"].astype(str).str[:4] + "-" + df_repasse["periodo"].astype(str).str[4:] + "-01")
    df_repasse['capital_join'] = padronizar_texto(df_repasse['cidade'])

    # 3. Base Safra 
    df_safra["data_referencia"] = pd.to_datetime(df_safra["ano"].astype(str) + "-" + df_safra["mes"].astype(str) + "-01")
    df_safra["producao_mensal_nacional"] = df_safra.groupby(["ano", "mes"])["quantidade_tons"].transform('sum')
    df_safra_nacional = df_safra[["data_referencia", "producao_mensal_nacional"]].drop_duplicates().reset_index(drop=True)

    # 4. Base Diesel
    df_diesel["data_referencia"] = df_diesel["data_da_coleta"].dt.to_period("M").dt.to_timestamp()
    capitais = ["aracaju", "belem", "belo_horizonte", "brasilia", "curitiba", "fortaleza", "goiania", "joao_pessoa", "natal", "porto_alegre", "recife", "rio_de_janeiro", "salvador", "sao_paulo", "vitoria", "florianopolis"]
    df_diesel['municipio_limpo'] = padronizar_texto(df_diesel['municipio'])
    df_diesel = df_diesel[df_diesel['municipio_limpo'].isin(capitais)]

    df_diesel_agrupado = df_diesel.pivot_table(
        index=["data_referencia", "municipio_limpo"],
        columns="produto",
        values=["valor_de_venda", "valor_de_venda_real"],
        aggfunc="mean"
    )
    df_diesel_agrupado.columns = [f"{a0}_{a1}" for a0, a1 in df_diesel_agrupado.columns]
    df_diesel_agrupado.reset_index(inplace=True)
    df_diesel_agrupado.rename(columns={'municipio_limpo': 'capital_join'}, inplace=True)

    # Médias dinâmicas blindadas a NaNs
    cols_real = df_diesel_agrupado.filter(like='valor_de_venda_real_DIESEL').columns
    df_diesel_agrupado['venda_real_diesel_media_geral'] = df_diesel_agrupado[cols_real].astype(float).mean(axis=1, skipna=True)

    cols_nom = df_diesel_agrupado.filter(regex='^valor_de_venda_DIESEL').columns
    df_diesel_agrupado['valor_venda_diesel_media_geral'] = df_diesel_agrupado[cols_nom].astype(float).mean(axis=1, skipna=True)

    df_diesel_agrupado.rename(columns={
        'valor_de_venda_real_DIESEL': 'venda_real_diesel_comum',
        'valor_de_venda_DIESEL': 'valor_venda_diesel_comum'
    }, inplace=True)


    print('Consolidando tabelas')
    
    df_unificado = df_precos.merge(df_safra_nacional, on="data_referencia", how="left")
    df_unificado = df_unificado.merge(df_diesel_agrupado, on=["data_referencia", "capital_join"], how="left")
    df_unificado = df_unificado.merge(df_repasse, on=["data_referencia", "capital_join"], how="left")

    # Limpeza de colunas redundantes
    colunas_remover = [c for c in df_unificado.columns if '_join' in c or c.endswith('_y')]
    df_unificado.drop(columns=colunas_remover, inplace=True)
    df_unificado.columns = df_unificado.columns.str.replace('_x', '')

    # Renomeação para melhorar o entendimento das colunas
    df_unificado.rename(columns={
        'codigo': 'codigo_cidade',
        'valor_repassado': 'valor_repassado_pbf',
        'valor_repassado_real': 'valor_repassado_pbf_real',
        'ln_valor_repassado_real': 'ln_valor_repassado_pbf_real',
        'preco_nominal': 'preco_nominal_feijao',
        'preco_real': 'preco_real_feijao',
        'log_preco_real': 'log_preco_feijao_real',
        'log_preco_nominal': 'log_preco_feijao_nominal',
        'var_pct_real': 'var_pct_ipca_real'
    }, inplace=True)

    ordem_desejada = [
        'data_referencia', 'capital_id', 'codigo_cidade', 'capital', 'uf', 'regiao',
        'preco_nominal_feijao', 'preco_real_feijao', 'log_preco_feijao_nominal', 'log_preco_feijao_real',
        'producao_mensal_nacional',
        'programa', 'qtd_familias', 'valor_repassado_pbf', 'valor_repassado_pbf_real', 'ln_valor_repassado_pbf_real',
        'valor_venda_diesel_comum', 'valor_de_venda_DIESEL S10', 'valor_de_venda_DIESEL S50', 'valor_venda_diesel_media_geral',
        'venda_real_diesel_comum', 'valor_de_venda_real_DIESEL S10', 'valor_de_venda_real_DIESEL S50', 'venda_real_diesel_media_geral',
        'ipca_indice', 'ipca_var_pct', 'ln_ipca_indice', 'var_pct_ipca_real'
    ]
    # Filtra colunas relevantes
    cols_finais = [c for c in ordem_desejada if c in df_unificado.columns]
    df_unificado = df_unificado[cols_finais]
    
    print("Salvando parquet")
    
    if salvar_parquet:
        print("Salvando Parquet em data/processed/consolidado")
        raiz = Path(__file__).resolve().parent.parent
        pasta_destino = raiz / "data" / "processed" / "consolidado"
        pasta_destino.mkdir(parents=True, exist_ok=True)
        
        arquivo_final = pasta_destino / "painel_feijao_consolidado.parquet"
        df_unificado.to_parquet(arquivo_final, index=False)
        print(f"Arquivo gerado em: {arquivo_final}")
    print("fim")
    return df_unificado

if __name__ == "__main__":
    consolidar_base_econometrica(salvar_parquet=True)