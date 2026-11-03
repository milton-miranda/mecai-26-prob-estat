import pandas as pd
from pathlib import Path
from huggingface_hub import hf_hub_download

# ==============================================================================
# MATRIZ OFICIAL DE COLHEITA DA CONAB (CALENDÁRIO AGRÍCOLA EXPANDIDO)
# ==============================================================================
calendario_conab_oficial = {
    'pr': {
        1: {12: 0.10, 1: 0.40, 2: 0.40, 3: 0.10},
        2: {4: 0.20, 5: 0.40, 6: 0.30, 7: 0.10},
        3: {8: 0.40, 9: 0.40, 10: 0.20} 
    },
    'sc': {
        1: {1: 0.20, 2: 0.40, 3: 0.30, 4: 0.10},
        2: {3: 0.10, 4: 0.40, 5: 0.40, 6: 0.10},
        3: {} 
    },
    'rs': {
        1: {1: 0.10, 2: 0.40, 3: 0.40, 4: 0.10},
        2: {3: 0.20, 4: 0.50, 5: 0.30},
        3: {}
    },
    'sp': {
        1: {11: 0.10, 12: 0.30, 1: 0.40, 2: 0.20},
        2: {3: 0.10, 4: 0.30, 5: 0.40, 6: 0.20},
        3: {7: 0.10, 8: 0.30, 9: 0.40, 10: 0.20} 
    },
    'mg': {
        1: {11: 0.10, 12: 0.40, 1: 0.40, 2: 0.10},
        2: {4: 0.10, 5: 0.40, 6: 0.40, 7: 0.10},
        3: {7: 0.10, 8: 0.30, 9: 0.40, 10: 0.20}
    },
    'rj': {
        1: {11: 0.20, 12: 0.50, 1: 0.30},
        2: {4: 0.20, 5: 0.50, 6: 0.30},
        3: {}
    },
    'es': {
        1: {11: 0.20, 12: 0.50, 1: 0.30},
        2: {4: 0.20, 5: 0.50, 6: 0.30},
        3: {}
    },
    'mt': {
        1: {1: 0.20, 2: 0.50, 3: 0.30},
        2: {5: 0.30, 6: 0.50, 7: 0.20},
        3: {7: 0.20, 8: 0.50, 9: 0.30}
    },
    'ms': {
        1: {12: 0.20, 1: 0.50, 2: 0.30},
        2: {4: 0.30, 5: 0.50, 6: 0.20},
        3: {7: 0.20, 8: 0.50, 9: 0.30}
    },
    'go': {
        1: {12: 0.20, 1: 0.50, 2: 0.30},
        2: {5: 0.20, 6: 0.50, 7: 0.30},
        3: {7: 0.20, 8: 0.50, 9: 0.30}
    },
    'df': {
        1: {12: 0.30, 1: 0.50, 2: 0.20},
        2: {7: 0.30, 8: 0.40, 9: 0.30}, 
        3: {8: 0.30, 9: 0.40, 10: 0.30}
    },
    'ba': {
        1: {3: 0.10, 4: 0.30, 5: 0.40, 6: 0.20},
        2: {8: 0.10, 9: 0.40, 10: 0.40, 11: 0.10},
        3: {6: 0.20, 7: 0.50, 8: 0.30} 
    },
    'ce': {
        1: {4: 0.20, 5: 0.50, 6: 0.30},
        2: {8: 0.20, 9: 0.50, 10: 0.30},
        3: {}
    },
    'pe': {
        1: {5: 0.20, 6: 0.50, 7: 0.30},
        2: {9: 0.20, 10: 0.50, 11: 0.30},
        3: {}
    }
}

def aplicar_calendario_pdf(df_max_anual):
    linhas_mensais = []
    
    # Mapa de conversão do nome completo (da base) para a sigla (do dicionário)
    mapa_para_sigla = {
        "acre": "ac", "amapa": "ap", "amazonas": "am", "para": "pa", "rondonia": "ro", 
        "roraima": "rr", "tocantins": "to", "alagoas": "al", "bahia": "ba", "ceara": "ce", 
        "maranhao": "ma", "paraiba": "pb", "pernambuco": "pe", "piaui": "pi", 
        "rio_grande_do_norte": "rn", "sergipe": "se", "distrito_federal": "df", 
        "goias": "go", "mato_grosso": "mt", "mato_grosso_do_sul": "ms", "espirito_santo": "es", 
        "minas_gerais": "mg", "rio_de_janeiro": "rj", "sao_paulo": "sp", "parana": "pr", 
        "rio_grande_do_sul": "rs", "santa_catarina": "sc"
    }
    
    for _, row in df_max_anual.iterrows():
        ano = row['ano']
        uf_completo = row['uf']
        sigla = mapa_para_sigla.get(uf_completo, "")
        safra = row['safra']
        volume = row['quantidade_tons']
        regiao = row['regiao']
        
        if volume == 0 or pd.isna(volume):
            continue
            
        distribuicao = {}
        # Agora a busca ocorre corretamente pela sigla!
        if sigla in calendario_conab_oficial:
            distribuicao = calendario_conab_oficial[sigla].get(safra, {})
            
        # Fallback de segurança (quase não será acionado agora)
        if not distribuicao:
            if regiao in ['Sul', 'Sudeste', 'Centro-Oeste']:
                if safra == 1: distribuicao = {11: 0.10, 12: 0.30, 1: 0.40, 2: 0.20}
                elif safra == 2: distribuicao = {4: 0.30, 5: 0.40, 6: 0.30}
                elif safra == 3: distribuicao = {7: 0.30, 8: 0.40, 9: 0.30} 
            else:
                if safra == 1: distribuicao = {4: 0.30, 5: 0.40, 6: 0.30}
                elif safra == 2: distribuicao = {8: 0.30, 9: 0.40, 10: 0.30}
                elif safra == 3: distribuicao = {6: 0.30, 7: 0.40, 8: 0.30}
                
        for mes, peso in distribuicao.items():
            ano_colhido = ano
            # A 1ª safra colhida em nov/dez pertence sempre ao ano anterior (civil)
            if safra == 1 and mes >= 11:
                ano_colhido = ano - 1
                
            linhas_mensais.append({
                'ano': ano_colhido,
                'mes': mes,
                'uf': uf_completo,  # Retorna com o nome longo para o Merge da Matriz OD funcionar
                'quantidade_tons': round(volume * peso, 0),
                'regiao': regiao
            })
            
    df_distribuido = pd.DataFrame(linhas_mensais)
    df_consolidado = df_distribuido.groupby(['ano', 'mes', 'uf', 'regiao'], observed=True, as_index=False)['quantidade_tons'].sum()
    return df_consolidado

def processar_dados_producao_feijao():
    caminho_raiz = Path.cwd().resolve()
    while not (caminho_raiz / "data").exists() and caminho_raiz.name != "":
        caminho_raiz = caminho_raiz.parent

    caminho_dados_inferidos = caminho_raiz / "data" / "raw" / "safra" / "producao_mensal_estimada_2004_2006.parquet"

    caminho_arquivo = hf_hub_download(
        repo_id="LeandroLDA/feijao_safra",
        filename="safra-area-producao-tons.csv",
        repo_type="dataset"
    )
    
    tem_inferencia = caminho_dados_inferidos.exists()
    
    if tem_inferencia:
        df_estimado_2004_2006 = pd.read_parquet(caminho_dados_inferidos)
        dic_regiao = {
            "acre": "Norte", "amapa": "Norte", "amazonas": "Norte", "para": "Norte", 
            "rondonia": "Norte", "roraima": "Norte", "tocantins": "Norte",
            "alagoas": "Nordeste", "bahia": "Nordeste", "ceara": "Nordeste", 
            "maranhao": "Nordeste", "paraiba": "Nordeste", "pernambuco": "Nordeste", 
            "piaui": "Nordeste", "rio_grande_do_norte": "Nordeste", "sergipe": "Nordeste",
            "distrito_federal": "Centro-Oeste", "goias": "Centro-Oeste", 
            "mato_grosso": "Centro-Oeste", "mato_grosso_do_sul": "Centro-Oeste",
            "espirito_santo": "Sudeste", "minas_gerais": "Sudeste", 
            "rio_de_janeiro": "Sudeste", "sao_paulo": "Sudeste",
            "parana": "Sul", "rio_grande_do_sul": "Sul", "santa_catarina": "Sul"
        }
        df_estimado_2004_2006['regiao'] = df_estimado_2004_2006['uf'].map(dic_regiao)
        
        # Filtro de transição que impede a sobreposição com perfeição
        mask_corte = (df_estimado_2004_2006['ano'] < 2005) | ((df_estimado_2004_2006['ano'] == 2005) & (df_estimado_2004_2006['mes'] <= 10))
        df_estimado_2004_2006 = df_estimado_2004_2006[mask_corte]
    else:
        print("Aviso: Dados inferidos (2004-2005) ainda não encontrados. Gerando painel parcial...")

    df = pd.read_csv(caminho_arquivo, header=3, index_col=False)
    
    colunas = pd.Series(df.columns)
    colunas.mask(df.columns.str.contains("Unnamed"), None, inplace=True)
    colunas = colunas.ffill()
    
    safras = df.iloc[0,:].astype(str).values
    df.columns = colunas + " " + safras
    df.drop(df.index[0], axis=0, inplace=True)
    df = df.rename(columns={df.columns[0]: "uf"})
    
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
    
    producao_tons_feijao = df.iloc[:27, :].copy()
    producao_long = producao_tons_feijao.melt(id_vars="uf", var_name="periodo_safra", value_name="quantidade_tons")
    producao_long["safra"] = producao_long["periodo_safra"].str.extract(r'(\d)_safra')
    
    # =====================================================================
    # CORREÇÃO TEMPORAL DEFINITIVA
    # Se o texto tiver barra (ex: 2006/07), a colheita = 2007 (ano base + 1)
    # Se o texto for limpo (ex: 2006), a colheita = 2006 (ano base)
    # =====================================================================
    ano_base = producao_long["periodo_safra"].str.extract(r'(\d{4})')[0].astype(int)
    tem_barra = producao_long["periodo_safra"].str.contains("/")
    producao_long["ano"] = ano_base + tem_barra.astype(int)
    
    producao_long.drop(columns=["periodo_safra"], inplace=True)
    producao_long["quantidade_tons"] = producao_long["quantidade_tons"].replace("-", "0")
    producao_long["quantidade_tons"] = pd.to_numeric(producao_long["quantidade_tons"], errors='coerce')
    producao_long = producao_long.dropna(subset=["quantidade_tons"])
    
    producao_long["uf"] = producao_long["uf"].astype("category")
    producao_long[["ano", "safra"]] = producao_long[["ano", "safra"]].astype(int)
    dic_regiao = {
        "acre": "Norte", "amapa": "Norte", "amazonas": "Norte", "para": "Norte", 
        "rondonia": "Norte", "roraima": "Norte", "tocantins": "Norte",
        "alagoas": "Nordeste", "bahia": "Nordeste", "ceara": "Nordeste", 
        "maranhao": "Nordeste", "paraiba": "Nordeste", "pernambuco": "Nordeste", 
        "piaui": "Nordeste", "rio_grande_do_norte": "Nordeste", "sergipe": "Nordeste",
        "distrito_federal": "Centro-Oeste", "goias": "Centro-Oeste", 
        "mato_grosso": "Centro-Oeste", "mato_grosso_do_sul": "Centro-Oeste",
        "espirito_santo": "Sudeste", "minas_gerais": "Sudeste", 
        "rio_de_janeiro": "Sudeste", "sao_paulo": "Sudeste",
        "parana": "Sul", "rio_grande_do_sul": "Sul", "santa_catarina": "Sul"
    }
    producao_long["regiao"] = producao_long["uf"].map(dic_regiao)

    producao_anual_real = (
        producao_long.groupby(["ano", "uf", "safra", "regiao"], observed=True, as_index=False)["quantidade_tons"]
        .max()
    )
    
    producao_mensal_agrupada = aplicar_calendario_pdf(producao_anual_real)
    producao_mensal_agrupada["is_estimado"] = False
    
    producao_mensal_agrupada = producao_mensal_agrupada[["ano", "mes", "uf", "regiao", "quantidade_tons", "is_estimado"]]
    
    if tem_inferencia:
        df_estimado_2004_2006 = df_estimado_2004_2006[["ano", "mes", "uf", "regiao", "quantidade_tons", "is_estimado"]]
        dataset_final_consolidado = pd.concat([df_estimado_2004_2006, producao_mensal_agrupada], ignore_index=True)
    else:
        dataset_final_consolidado = producao_mensal_agrupada

    dataset_final_consolidado = dataset_final_consolidado.sort_values(by=["ano", "mes", "uf"]).reset_index(drop=True)
    
    caminho_saida = caminho_raiz / "data" / "interim" / "safra"
    caminho_saida.mkdir(parents=True, exist_ok=True)
    
    arquivo_saida = caminho_saida / "producao_feijao_tons.parquet"
    dataset_final_consolidado.to_parquet(arquivo_saida, index=False)
    
    return dataset_final_consolidado