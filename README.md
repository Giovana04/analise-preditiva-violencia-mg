# Análise da Violência Doméstica em Minas Gerais (2014–2023)

> Pipeline completo de Engenharia de Dados, Análise Exploratória e Machine Learning aplicado a dados públicos da violência doméstica em Minas Gerais.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.x-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)

---

# Sobre o projeto

Este projeto utiliza dados públicos de ocorrências de violência doméstica registrados em Minas Gerais entre **2014 e 2023** para construir um pipeline completo de Ciência de Dados.

O objetivo não é apenas produzir gráficos, mas desenvolver uma solução completa envolvendo:

- Engenharia de Dados
- ETL
- Banco de Dados Relacional
- SQL
- Análise Exploratória
- Engenharia de Atributos
- Machine Learning
- Implementação matemática de Regressão Ridge utilizando apenas NumPy

---

# Objetivos

- Consolidar arquivos CSV anuais em uma base única.
- Construir um banco de dados relacional utilizando SQLite.
- Explorar padrões temporais e espaciais.
- Identificar tendências na violência doméstica.
- Demonstrar implementação matemática da Regressão Ridge.

---

# Tecnologias

- Python
- Pandas
- NumPy
- SQLite
- SQLAlchemy
- Matplotlib
- Seaborn
- Scikit-Learn

--- 

# Pipeline

CSV

↓

ETL

↓

Modelo Relacional

↓

SQLite

↓

SQL

↓

EDA

↓

Feature Engineering

↓

Machine Learning

↓

Resultados

---

# Modelo Relacional

- Dim_Municipio
- Dim_Natureza
- Fato_Ocorrencia

---

# Principais análises

- Evolução temporal
- Distribuição por município
- Natureza dos delitos
- Comparação RMBH × Interior
- Distribuição mensal
- Estatísticas descritivas
- Correlações

---

# Machine Learning

O projeto apresenta dois estudos:

## Regressão Logística

Classificação exploratória de ocorrências.

## Regressão Ridge

Implementação manual utilizando:

- Álgebra Linear
- Gradiente Descendente Estocástico
- Penalização L2
- NumPy puro

---

# Resultados

- Consolidação de quase 1 milhão de registros.
- Banco relacional normalizado.
- Pipeline ETL reutilizável.
- Implementação matemática da Ridge Regression.
- Análise temporal da evolução da violência doméstica.

---

# Como executar

```bash
git clone ...

cd analise-violencia-mg

pip install -r requirements.txt

jupyter notebook
```

---

# Trabalhos futuros

- Integração com dados do IBGE
- Dashboards em Streamlit
- Mapas utilizando GeoPandas
- Clusterização espacial
- Séries temporais
- Modelos baseados em árvores (Random Forest, XGBoost)
