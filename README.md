# Violência doméstica em Minas Gerais (2014–2023)

Pipeline de dados de ponta a ponta sobre quase **1 milhão de registros** públicos de ocorrências: ETL de CSVs anuais para um banco relacional, análise com SQL, e um estudo de regressão Ridge comparando o scikit-learn com uma implementação própria em NumPy.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?logo=sqlite&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)

## O que o projeto mostra

- **Engenharia de dados:** consolida 10 CSVs anuais (cerca de 990 mil linhas), limpa e tipa as colunas e carrega um modelo dimensional em SQLite.
- **SQL para análise:** as métricas são agregadas no banco antes de irem para o Pandas.
- **Estatística aplicada:** testa três hipóteses de negócio e mostra por que a multicolinearidade atrapalha a interpretação de um modelo linear.
- **Fundamentos de ML:** regressão Ridge com gradiente descendente estocástico implementada só com NumPy e comparada com o scikit-learn.

## Principais achados

| Pergunta | Resultado |
|---|---|
| O volume cresce de forma constante? | Fica em torno de 150 mil vítimas por ano até 2022. A queda em 2023 (a base tem 61,5 mil registros, contra cerca de 103 mil nos outros anos) parece ser consolidação incompleta dos dados, não redução real. |
| A capital concentra a violência? | Não. O interior do estado responde por **74,0%** das ocorrências e a Região Metropolitana de BH por 26,0%. |
| Ameaça e lesão corporal andam juntas? | Sim. A correlação entre ameaças e agressão física por município é de **0,99**, e entre ameaças e quebra de medida protetiva é de 0,91. |

## Pipeline

```mermaid
flowchart LR
    A[CSVs anuais<br/>2014-2023] --> B[ETL<br/>src/etl_builder.py]
    B --> C[(SQLite<br/>modelo dimensional)]
    C --> D[Consultas SQL]
    D --> E[Análise exploratória]
    E --> F[Features e Ridge<br/>scikit-learn x NumPy]
```

### Modelo de dados

| Tabela | Conteúdo |
|---|---|
| `Dim_Municipio` | código e nome do município, RISP e indicador de Região Metropolitana (`is_rmbh`) |
| `Dim_Natureza` | tipo de delito e categoria agrupada (Ameaça, Agressão Física, Quebra de Medida, Crime Sexual, Crime Letal, Outros) |
| `Fato_Ocorrencia` | data, mês, trimestre, ano, tentado/consumado e quantidade de vítimas |

## Regressão Ridge: scikit-learn x NumPy

O alvo é o total de agressões físicas por município, explicado por ameaças, quebras de medida protetiva e a interação entre as duas, com as variáveis padronizadas e `alpha = 10`.

A implementação própria (`src/custom_ridge.py`) usa gradiente descendente estocástico com penalidade L2. Com 50 mil épocas, ela **não chegou aos mesmos coeficientes** do scikit-learn, que usa o solver SAG: no peso de "Ameaças" o scikit-learn ficou perto de 803 e a versão em NumPy perto de 92. O notebook discute o motivo: com variáveis tão correlacionadas, a função de custo forma um vale estreito em que o SGD simples oscila ou avança muito devagar. A conclusão do estudo é que, nesse cenário, os coeficientes isolados não devem ser lidos como efeito de cada variável.

## Estrutura do repositório

```
├── data/           CSVs anuais (2014-2023)
├── notebooks/      análise completa (analise_de_violencia_mg.ipynb)
├── src/
│   ├── etl_builder.py    leitura, limpeza, modelo dimensional e carga no SQLite
│   └── custom_ridge.py   regressão Ridge com SGD em NumPy
└── requirements.txt
```

## Como executar

```bash
git clone https://github.com/Giovana04/analise-preditiva-violencia-mg.git
cd analise-preditiva-violencia-mg

python -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -r requirements.txt jupyter

jupyter notebook notebooks/analise_de_violencia_mg.ipynb
```

Ao rodar a primeira célula, o notebook executa o ETL e gera o arquivo `violencia_mg.sqlite` na raiz do projeto.

## Limitações

- A base de 2023 está incompleta, então comparações com esse ano devem ser feitas com cuidado.
- O modelo é exploratório: serve para estudar multicolinearidade e otimização, não para prever ocorrências.
- A análise é agregada por município, sem ajuste por população.

## Próximos passos

- Cruzar com dados do IBGE para analisar taxas por habitante.
- Substituir o SGD simples por um otimizador com momento e comparar a convergência.
- Mapas com GeoPandas e dashboard em Streamlit.
