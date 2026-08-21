# Análise de inflação do PBF no preço de Feijão

Projeto de análise econométrica de séries temporais destinado a investigar a relação entre o **Programa Bolsa Família (PBF)** e a dinâmica do **preço do feijão**, com ênfase na avaliação de possíveis efeitos inflacionários associados às transferências do programa.

O repositório organiza todo o fluxo da pesquisa, desde a aquisição e preparação dos dados até a estimação dos modelos econométricos, diagnóstico, análise dos resultados, geração de figuras e produção do relatório final.

> **Status:** Em desenvolvimento
> **Tipo de análise:** Econometria de séries temporais
> **Linguagem principal:** Python

---

## 1. Objetivo do projeto

O objetivo geral é desenvolver uma análise econométrica da relação temporal entre os recursos associados ao Programa Bolsa Família e o preço do feijão.

O projeto deverá investigar questões como:

* evolução temporal do preço do feijão;
* evolução temporal das variáveis relacionadas ao PBF;
* tendência, sazonalidade e ciclos presentes nas séries;
* propriedades de estacionariedade e ordem de integração;
* relações dinâmicas entre as variáveis;
* existência de relações de curto e longo prazo;
* cointegração entre séries, quando aplicável;
* precedência temporal por meio de testes de causalidade de Granger;
* respostas do preço do feijão a choques nas variáveis relacionadas ao PBF;
* importância relativa dos diferentes choques para a variação das séries;
* estabilidade das relações ao longo do período analisado;
* capacidade preditiva dos modelos estimados.

A interpretação dos resultados deverá distinguir cuidadosamente **associação temporal, precedência temporal e evidência causal**. A existência de correlação ou causalidade de Granger, isoladamente, não será interpretada como demonstração de que o PBF causa inflação no preço do feijão.

---

# 2. Estrutura do repositório

```text
econometric-time-series-pbf-feijao/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── dictionary/
│
├── notebooks/
│   ├── 00_setup.ipynb
│   ├── 01_data_ingestion_cleaning.ipynb
│   ├── 02_exploratory_time_series.ipynb
│   ├── 03_time_series_diagnostics.ipynb
│   ├── 04_stationarity_unit_roots.ipynb
│   ├── 05_univariate_models.ipynb
│   ├── 06_multivariate_models.ipynb
│   ├── 07_cointegration_vecm.ipynb
│   ├── 08_granger_irf_fevd.ipynb
│   ├── 09_volatility_models.ipynb
│   ├── 10_forecasting_backtesting.ipynb
│   ├── 11_model_comparison.ipynb
│   └── 12_final_results.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── preprocessing.py
│   ├── time_features.py
│   ├── diagnostics.py
│   ├── stationarity.py
│   ├── cointegration.py
│   ├── causality.py
│   ├── structural_breaks.py
│   ├── forecasting.py
│   ├── backtesting.py
│   ├── evaluation.py
│   │
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── figures.py
│   │
│   └── models/
│       ├── __init__.py
│       ├── baseline.py
│       ├── arima.py
│       ├── sarima.py
│       ├── exponential_smoothing.py
│       ├── var.py
│       ├── svar.py
│       ├── vecm.py
│       ├── arch_garch.py
│       ├── dynamic_regression.py
│       └── forecast_models.py
│
├── figures/
│   ├── exploratory/
│   ├── diagnostics/
│   ├── stationarity/
│   ├── cointegration/
│   ├── causality/
│   ├── impulse_response/
│   ├── volatility/
│   ├── forecasting/
│   ├── model_performance/
│   └── final/
│
├── reports/
│   ├── technical/
│   ├── tables/
│   └── final_report/
│
└── docs/
    ├── project_description.md
    ├── analysis_plan.md
    ├── econometric_specifications.md
    ├── variable_dictionary.md
    ├── model_specifications.md
    └── validation_strategy.md
```

---

# 3. Organização dos dados

## `data/raw/`

Contém os **dados originais**, exatamente como foram obtidos das respectivas fontes.

Exemplos:

* séries históricas do preço do feijão;
* informações referentes ao PBF;
* índices de preços;
* variáveis macroeconômicas;
* variáveis agrícolas;
* dados climáticos;
* séries utilizadas como controles.

Os arquivos desta pasta **não devem ser alterados manualmente**.

Toda transformação deverá produzir um novo arquivo em `interim/` ou `processed/`.

---

## `data/interim/`

Contém dados intermediários produzidos durante o processo de preparação.

Exemplos:

* dados com datas padronizadas;
* séries convertidas para frequência mensal;
* junções entre diferentes bases;
* tratamentos preliminares de missing values;
* séries deflacionadas;
* transformações temporárias.

Esses dados podem ser recriados a partir de `data/raw/`.

---

## `data/processed/`

Contém os datasets finais utilizados na estimação dos modelos.

Exemplos:

* dataset econométrico consolidado;
* séries transformadas;
* logaritmos;
* primeiras diferenças;
* taxas de crescimento;
* variáveis defasadas;
* séries deflacionadas;
* variáveis de controle;
* datasets específicos para VAR, VECM ou forecasting.

Idealmente, qualquer resultado econométrico apresentado no projeto deve poder ser reproduzido a partir dos dados presentes nesta pasta.

---

## `data/dictionary/`

Contém documentação sobre os dados.

Devem ser registrados:

* nome da variável;
* descrição;
* unidade;
* frequência;
* período disponível;
* fonte;
* URL ou identificador da fonte;
* data de extração;
* transformação realizada;
* observações metodológicas.

Essa documentação é fundamental para a reprodutibilidade da análise.

---

# 4. Notebooks

Os notebooks representam a sequência analítica da pesquisa.

Eles devem funcionar principalmente como **orquestradores da análise**. Funções reutilizáveis devem ser implementadas em `src/` e importadas pelos notebooks.

## `00_setup.ipynb`

Configuração inicial do projeto.

Responsabilidades:

* localizar a raiz do projeto;
* configurar imports;
* verificar versões;
* configurar caminhos;
* testar dependências;
* validar acesso aos diretórios.

---

## `01_data_ingestion_cleaning.ipynb`

Aquisição, integração e preparação inicial dos dados.

Inclui:

* leitura das bases;
* padronização das datas;
* identificação de missing values;
* identificação de duplicatas;
* compatibilização das frequências;
* integração das diferentes fontes;
* validação temporal;
* geração dos datasets intermediários.

---

## `02_exploratory_time_series.ipynb`

Análise exploratória das séries.

Inclui:

* estatísticas descritivas;
* gráficos temporais;
* distribuições;
* tendência;
* sazonalidade;
* decomposição temporal;
* correlações;
* comparação visual entre séries.

---

## `03_time_series_diagnostics.ipynb`

Diagnóstico das propriedades temporais.

Inclui:

* ACF;
* PACF;
* autocorrelação;
* sazonalidade;
* análise de resíduos;
* identificação preliminar de mudanças estruturais.

---

## `04_stationarity_unit_roots.ipynb`

Análise de estacionariedade e raízes unitárias.

Podem ser utilizados testes como:

* ADF;
* KPSS;
* Phillips-Perron;
* testes adicionais quando metodologicamente necessários.

Esse notebook deverá determinar a ordem de integração das séries antes da especificação dos modelos multivariados.

---

## `05_univariate_models.ipynb`

Modelagem individual das séries.

Possíveis modelos:

* AR;
* MA;
* ARMA;
* ARIMA;
* SARIMA;
* exponential smoothing.

Esses modelos também poderão servir como benchmarks para avaliações posteriores.

---

## `06_multivariate_models.ipynb`

Modelagem conjunta das séries.

Principalmente:

* VAR;
* SVAR;
* regressões dinâmicas;
* modelos com variáveis exógenas.

---

## `07_cointegration_vecm.ipynb`

Investigação de relações de equilíbrio de longo prazo.

Inclui:

* Engle-Granger;
* Johansen;
* determinação do rank de cointegração;
* estimação de VECM;
* interpretação dos mecanismos de correção de erro.

---

## `08_granger_irf_fevd.ipynb`

Análise das relações dinâmicas entre as variáveis.

Inclui:

* causalidade de Granger;
* Impulse Response Functions — IRF;
* Forecast Error Variance Decomposition — FEVD;
* interpretação econômica dos choques.

Este notebook será particularmente importante para investigar como choques associados às variáveis do PBF se relacionam dinamicamente com o preço do feijão.

---

## `09_volatility_models.ipynb`

Análise da volatilidade das séries quando aplicável.

Possíveis modelos:

* ARCH;
* GARCH;
* extensões da família GARCH.

---

## `10_forecasting_backtesting.ipynb`

Avaliação out-of-sample.

Inclui:

* divisão temporal treino/teste;
* expanding window;
* rolling window;
* previsões multi-step;
* comparação com benchmarks;
* avaliação da estabilidade das previsões.

---

## `11_model_comparison.ipynb`

Comparação sistemática entre modelos.

Possíveis métricas:

* MAE;
* RMSE;
* MAPE;
* sMAPE;
* MASE;
* AIC;
* BIC.

Quando apropriado, podem ser utilizados testes estatísticos de comparação de capacidade preditiva, como Diebold-Mariano.

---

## `12_final_results.ipynb`

Consolidação dos resultados finais.

Este notebook deverá reunir:

* principais tabelas;
* figuras finais;
* resultados econométricos;
* comparação entre modelos;
* interpretação econômica;
* limitações;
* conclusões.

---

# 5. Código-fonte — `src/`

A pasta `src/` contém o código reutilizável do projeto.

O princípio adotado é:

```text
notebooks → executam a análise
src       → implementa a análise
```

Isso reduz duplicação de código e melhora a reprodutibilidade.

### Principais módulos

`preprocessing.py`
Limpeza e transformação dos dados.

`time_features.py`
Construção de características temporais, lags, diferenças e transformações.

`diagnostics.py`
Diagnósticos gerais de séries temporais e modelos.

`stationarity.py`
Testes de estacionariedade e raízes unitárias.

`cointegration.py`
Testes e ferramentas relacionadas à cointegração.

`causality.py`
Testes de causalidade e relações temporais.

`structural_breaks.py`
Análise de quebras estruturais.

`forecasting.py`
Rotinas de previsão.

`backtesting.py`
Rolling window, expanding window e avaliação out-of-sample.

`evaluation.py`
Métricas e comparação dos modelos.

---

# 6. Modelos — `src/models/`

Implementações específicas dos modelos devem permanecer separadas.

```text
models/
├── baseline.py
├── arima.py
├── sarima.py
├── exponential_smoothing.py
├── var.py
├── svar.py
├── vecm.py
├── arch_garch.py
├── dynamic_regression.py
└── forecast_models.py
```

Essa organização permite acrescentar novos modelos sem modificar os notebooks principais.

---

# 7. Figuras — `figures/`

As figuras geradas pelas análises devem ser salvas automaticamente de acordo com sua finalidade.

```text
figures/
├── exploratory/          # análise exploratória
├── diagnostics/          # diagnósticos
├── stationarity/         # estacionariedade
├── cointegration/        # cointegração
├── causality/            # causalidade de Granger
├── impulse_response/     # IRF e FEVD
├── volatility/           # volatilidade
├── forecasting/          # previsões
├── model_performance/    # comparação dos modelos
└── final/                # figuras selecionadas para relatório
```

Evite salvar manualmente figuras em locais arbitrários.

---

# 8. Relatórios — `reports/`

## `reports/technical/`

Resultados técnicos detalhados.

Exemplos:

* diagnósticos;
* outputs completos;
* especificações;
* resultados intermediários.

## `reports/tables/`

Tabelas exportadas pelos notebooks.

Exemplos:

* estatísticas descritivas;
* testes de estacionariedade;
* critérios de informação;
* testes de cointegração;
* resultados VAR/VECM;
* causalidade de Granger;
* métricas de forecasting.

## `reports/final_report/`

Versões finais dos relatórios da pesquisa.

---

# 9. Documentação — `docs/`

A documentação metodológica deve ser mantida separada do código.

`project_description.md`
Descrição e motivação da pesquisa.

`analysis_plan.md`
Plano de análise e sequência das etapas.

`econometric_specifications.md`
Especificações econométricas consideradas.

`variable_dictionary.md`
Descrição das variáveis.

`model_specifications.md`
Configuração dos modelos utilizados.

`validation_strategy.md`
Procedimentos de validação e avaliação out-of-sample.

---

# 10. Clonando o repositório

Primeiro escolha onde deseja armazenar o projeto.

No Windows/PowerShell:

```powershell
cd "C:\Users\SEU_USUARIO\Documents"
```

Clone:

```powershell
git clone <URL-DO-REPOSITORIO>
```

Entre na pasta:

```powershell
cd econometric-time-series-pbf-feijao
```

---

# 11. Criando o ambiente Python

Recomenda-se utilizar um ambiente virtual independente para o projeto.

No Windows:

```powershell
python -m venv .venv
```

Ative:

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando ativado, o terminal deverá apresentar algo semelhante a:

```text
(.venv) PS C:\...\econometric-time-series-pbf-feijao>
```

Atualize o `pip`:

```powershell
python -m pip install --upgrade pip
```

---

# 12. Instalando as dependências

Com a `.venv` ativada:

```powershell
pip install -r requirements.txt
```

Entre as principais bibliotecas previstas para o projeto estão:

* NumPy;
* pandas;
* SciPy;
* statsmodels;
* arch;
* scikit-learn;
* Matplotlib;
* Plotly;
* Jupyter;
* openpyxl;
* PyArrow;
* pytest.

As versões utilizadas no estudo devem ser registradas no `requirements.txt` para permitir a reprodução do ambiente.

---

# 13. Configurando o Jupyter

Com o ambiente ativado:

```powershell
pip install ipykernel
```

Registre o ambiente:

```powershell
python -m ipykernel install --user --name pbf-feijao --display-name "Python - PBF Feijao"
```

Depois abra:

```powershell
jupyter lab
```

ou utilize os notebooks diretamente pelo VS Code.

Selecione o kernel:

```text
Python - PBF Feijao
```

---

# 14. Como iniciar a análise

A análise deve seguir a ordem numérica dos notebooks.

```text
00_setup
    ↓
01_data_ingestion_cleaning
    ↓
02_exploratory_time_series
    ↓
03_time_series_diagnostics
    ↓
04_stationarity_unit_roots
    ↓
05_univariate_models
    ↓
06_multivariate_models
    ↓
07_cointegration_vecm
    ↓
08_granger_irf_fevd
    ↓
09_volatility_models
    ↓
10_forecasting_backtesting
    ↓
11_model_comparison
    ↓
12_final_results
```

Antes de executar os modelos econométricos, deve-se garantir que:

1. as fontes de dados estejam documentadas;
2. a frequência temporal esteja corretamente definida;
3. as datas estejam alinhadas;
4. missing values tenham sido avaliados;
5. transformações estejam documentadas;
6. as propriedades de estacionariedade tenham sido investigadas;
7. a ordem de integração das séries seja conhecida.

---

# 15. Adicionando dados ao projeto

Os dados originais devem ser colocados em:

```text
data/raw/
```

Nunca altere os arquivos originais.

O fluxo recomendado é:

```text
Fonte externa
      ↓
data/raw/
      ↓
limpeza e padronização
      ↓
data/interim/
      ↓
transformações econométricas
      ↓
data/processed/
      ↓
modelagem
```

Arquivos de dados muito grandes, restritos ou que possam conter informações sensíveis **não devem ser enviados ao GitHub**.

---

# 16. Fluxo Git recomendado

Antes de iniciar uma alteração:

```powershell
git pull
```

Depois de realizar alterações:

```powershell
git status
```

Adicione:

```powershell
git add .
```

Faça o commit:

```powershell
git commit -m "Descrição da alteração"
```

E envie:

```powershell
git push
```

Exemplos de commits:

```text
feat: add PBF data ingestion
feat: implement stationarity tests
feat: implement VAR models
feat: add Johansen cointegration analysis
feat: implement Granger causality analysis
feat: add rolling window backtesting

fix: correct monthly date alignment
fix: handle missing observations

docs: update variable dictionary
docs: document econometric methodology
```

---

# 17. Reprodutibilidade

Toda análise relevante deve ser reproduzível a partir do conteúdo do repositório.

Evite:

* caminhos absolutos específicos de um computador;
* edição manual dos datasets processados;
* números inseridos manualmente nos resultados;
* figuras editadas externamente sem documentação;
* código importante existente somente em notebooks.

Prefira:

* caminhos relativos;
* funções em `src/`;
* configuração centralizada;
* seeds quando aplicáveis;
* geração automática de tabelas;
* geração automática de figuras;
* datasets processados produzidos por código.

---

# 18. Convenções do projeto

## Dados

```text
raw       → dados originais
interim   → dados intermediários
processed → dados prontos para análise
dictionary → metadados e dicionários
```

## Código

```text
src/ → código reutilizável
```

## Experimentação

```text
notebooks/ → execução e documentação das análises
```

## Resultados gráficos

```text
figures/
```

## Resultados tabulares e relatórios

```text
reports/
```

## Documentação metodológica

```text
docs/
```

---

# 19. Princípios metodológicos

O projeto deve preservar uma separação clara entre:

**Descrição**

> Como o preço do feijão e as variáveis relacionadas ao PBF evoluíram no tempo?

**Associação**

> Existe associação estatística entre essas séries?

**Dinâmica temporal**

> Valores passados de uma variável ajudam a explicar valores futuros de outra?

**Relações de longo prazo**

> As séries apresentam uma relação de equilíbrio de longo prazo?

**Choques**

> Como o preço do feijão responde dinamicamente a um choque em uma variável associada ao PBF?

**Previsão**

> A inclusão das variáveis relacionadas ao PBF melhora a previsão out-of-sample do preço do feijão?

**Causalidade econômica**

> A evidência disponível permite atribuir mudanças no preço do feijão ao PBF, após considerar fatores concorrentes e possíveis problemas de identificação?

Essa separação é importante para evitar conclusões causais que não sejam sustentadas pelo desenho econométrico.

---

# 20. Resultado esperado

Ao final do projeto, espera-se obter um pipeline reproduzível capaz de produzir:

* base econométrica consolidada;
* análise exploratória;
* diagnóstico das séries;
* testes de estacionariedade;
* modelos univariados;
* modelos multivariados;
* análise de cointegração;
* VECM, quando aplicável;
* causalidade de Granger;
* funções impulso-resposta;
* decomposição da variância;
* análise de volatilidade, quando pertinente;
* forecasting;
* backtesting;
* comparação de modelos;
* tabelas econométricas;
* figuras;
* relatório final.

---

## Licença

Definir a licença do projeto antes da distribuição pública do código e dos dados.

## Autor

Projeto desenvolvido no contexto de estudos em Probabilidade, Estatística e Econometria.
