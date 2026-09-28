import pandas as pd
from pathlib import Path
from huggingface_hub import hf_hub_download

def processar_dados_producao_feijao():
    """
    Baixa os dados brutos de producao do feijao do Hugging Face,
    realiza a limpeza, formatação (transpõe colunas em linhas) 
    e salva o resultado em formato .parquet na pasta data/processed/producao_feijao/.
    """

    caminho_arquivo = hf_hub_download(
        repo_id="LeandroLDA/feijao_safra",
        filename="safra-area-producao-tons.csv",
        repo_type="dataset"
    )
    
    df = pd.read_csv(caminho_arquivo, header=3, index_col=False)
    
    colunas = pd.Series(df.columns)
    colunas.mask(df.columns.str.contains("Unnamed"), None, inplace=True)
    colunas = colunas.ffill()
    
    safras = df.iloc[0,:].astype(str).values
    df.columns = colunas + " " + safras
    df.drop(df.index[0], axis=0, inplace=True)
    df = df.rename(columns={df.columns[0]: "uf"})
    
    # Tratamento dos nomes das colunas
    colunas = pd.Series(df.columns)
    colunas = (
        colunas
        .str.replace(r'\d+\.\d+\s', "", regex=True)
        .str.replace("Feijão", "")
        .str.replace(r"ª\n", r' safra', regex=True)
        .str.replace(r"ª", r' safra', regex=True) 
        .str.lower()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.replace(r"\s+", "_", regex=True) 
        .str.strip("_")
    )
    df.columns = colunas
    
    df["uf"] = (
        df["uf"]
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )
    
    # Filtrando apenas as linhas dos estados (cortando dados desnecessários no fim do arquivo)
    producao_tons_feijao = df.iloc[:27, :].copy()
    
    producao_long = producao_tons_feijao.melt(
        id_vars="uf",
        var_name="periodo_safra",
        value_name="quantidade_tons"
    )
    
    # # Extraindo mês, ano e safra
    # producao_long[["mes", "ano", "safra", "descartar"]] = producao_long.periodo_safra.str.split("_", expand=True)
    # producao_long.drop(columns=["periodo_safra", "descartar"], inplace=True)
    
    # Extraindo mês, ano e safra com regex
    producao_long["mes"] = producao_long["periodo_safra"].str.extract(r'([a-z]+)')
    producao_long["ano"] = producao_long["periodo_safra"].str.extract(r'(\d{4})')
    producao_long["safra"] = producao_long["periodo_safra"].str.extract(r'(\d)_safra')
    producao_long.drop(columns=["periodo_safra"], inplace=True)
    
    # Tratamento de valores numéricos
    producao_long["quantidade_tons"] = producao_long["quantidade_tons"].replace("-", "0")
    producao_long["quantidade_tons"] = pd.to_numeric(producao_long["quantidade_tons"], errors='coerce')
    producao_long = producao_long.dropna(subset=["quantidade_tons"])
    
    producao_long["uf"] = producao_long["uf"].astype("category")
    producao_long[["ano", "safra"]] = producao_long[["ano", "safra"]].astype(int)
    
    # Mapeamento de meses
    dic_meses = {
        "janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4,
        "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
        "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
    }
    
    dic_regiao = {
    # Região Norte
    "acre": "Norte",
    "amapa": "Norte",
    "amazonas": "Norte",
    "para": "Norte",
    "rondonia": "Norte",
    "roraima": "Norte",
    "tocantins": "Norte",
    
    # Região Nordeste
    "alagoas": "Nordeste",
    "bahia": "Nordeste",
    "ceara": "Nordeste",
    "maranhao": "Nordeste",
    "paraiba": "Nordeste",
    "pernambuco": "Nordeste",
    "piaui": "Nordeste",
    "rio_grande_do_norte": "Nordeste",
    "sergipe": "Nordeste",
    
    # Região Centro-Oeste
    "distrito_federal": "Centro-Oeste",
    "goias": "Centro-Oeste",
    "mato_grosso": "Centro-Oeste",
    "mato_grosso_do_sul": "Centro-Oeste",
    
    # Região Sudeste
    "espirito_santo": "Sudeste",
    "minas_gerais": "Sudeste",
    "rio_de_janeiro": "Sudeste",
    "sao_paulo": "Sudeste",
    
    # Região Sul
    "parana": "Sul",
    "rio_grande_do_sul": "Sul",
    "santa_catarina": "Sul"
}
    
    producao_long["mes"] = (
        producao_long["mes"]
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )
    
    # Mapeamento dos meses e regiões
    producao_long["mes"] = producao_long["mes"].map(dic_meses)
    producao_long["regiao"] = producao_long["uf"].map(dic_regiao)
    
    # Organizando as colunas finais
    producao_long = producao_long[["ano", "mes", "uf", "safra", "quantidade_tons", "regiao"]]
    producao_long = producao_long.sort_values(by=["ano", "mes", "uf"]).reset_index(drop=True)
    
    # Salvando em formato Parquet no diretório
    raiz_projeto = Path(__file__).parent.parent 
    caminho_saida = raiz_projeto / "data" / "interim" / "safra"
    caminho_saida.mkdir(parents=True, exist_ok=True)
    
    arquivo_saida = caminho_saida / "producao_feijao_tons.parquet"
    producao_long.to_parquet(arquivo_saida, index=False)
    
    return producao_long