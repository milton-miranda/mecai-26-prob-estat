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
        repo_id="pbf-feijao-mecai-usp/bf-feijao-dados",
        filename="raw/painel_feijao_deflacionado.csv",
        repo_type="dataset"
    )
    
    df = pd.read_csv(caminho_arquivo)
    
    
    # Dicionário mapeando a Capital para o seu respectivo Estado
    dic_capital_estado = {
        # Norte
        "rio_branco": "acre",
        "macapa": "amapa",
        "manaus": "amazonas",
        "belem": "para",
        "porto_velho": "rondonia",
        "boa_vista": "roraima",
        "palmas": "tocantins",
        
        # Nordeste
        "maceio": "alagoas",
        "salvador": "bahia",
        "fortaleza": "ceara",
        "sao_luis": "maranhao",
        "joao_pessoa": "paraiba",
        "recife": "pernambuco",
        "teresina": "piaui",
        "natal": "rio_grande_do_norte",
        "aracaju": "sergipe",
        
        # Centro-Oeste
        "brasilia": "distrito_federal",
        "goiania": "goias",
        "cuiaba": "mato_grosso",
        "campo_grande": "mato_grosso_do_sul",
        
        # Sudeste
        "vitoria": "espirito_santo",
        "belo_horizonte": "minas_gerais",
        "rio_de_janeiro": "rio_de_janeiro",
        "sao_paulo": "sao_paulo",
        
        # Sul
        "curitiba": "parana",
        "porto_alegre": "rio_grande_do_sul",
        "florianopolis": "santa_catarina"
    }
    
     # Salvando em formato Parquet no diretório
    raiz_projeto = Path(__file__).parent.parent 
    caminho_saida = raiz_projeto / "data" / "interim" / "precos_feijao_def"
    caminho_saida.mkdir(parents=True, exist_ok=True)
        
    arquivo_saida = caminho_saida / "precos_feijao_deflacionado.parquet"
    df.to_parquet(arquivo_saida, index=False)
    
    
    
    
    
    return df