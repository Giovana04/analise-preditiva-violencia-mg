import pandas as pd
import sqlalchemy as sqla
from pathlib import Path

def carregar_dados_brutos(data_dir: Path, ano_inicio=2014, ano_fim=2023):
    dataframes = []
    for ano in range(ano_inicio, ano_fim + 1):
        arquivo = data_dir / f'violencia_domestica_{ano}.csv'
        if arquivo.exists():
            try:
                df = pd.read_csv(arquivo, sep=';', encoding='utf-8-sig', parse_dates=['data_fato'], na_values=['-', 'NA'])
            except UnicodeDecodeError:
                df = pd.read_csv(arquivo, sep=';', encoding='latin1', parse_dates=['data_fato'], na_values=['-', 'NA'])
            
            df.columns = df.columns.str.replace('^\ufeff', '', regex=True).str.strip().str.lower()
            
            # Aplica a tipagem apenas DEPOIS de ter limpado os nomes das colunas
            if 'municipio_cod' in df.columns:
                df['municipio_cod'] = pd.to_numeric(df['municipio_cod'], errors='coerce').astype('Int64')
            if 'municipio_fato' in df.columns:
                df['municipio_fato'] = df['municipio_fato'].astype('string')
                
            dataframes.append(df)
    
    if not dataframes:
        raise FileNotFoundError("Nenhum CSV encontrado na pasta 'data'.")
        
    return pd.concat(dataframes, ignore_index=True)

def processar_modelo_relacional(df):    
    dim_municipio = df[['municipio_cod', 'municipio_fato', 'risp', 'rmbh']].drop_duplicates(subset=['municipio_cod']).copy()
    dim_municipio = dim_municipio.rename(columns={'municipio_cod': 'id_municipio', 'municipio_fato': 'nome'})
    dim_municipio['is_rmbh'] = dim_municipio['rmbh'].apply(lambda x: 0 if pd.isna(x) or 'Interior' in str(x) else 1)
    dim_municipio = dim_municipio.dropna(subset=['id_municipio'])
    
    naturezas_unicas = df['natureza_delito'].dropna().unique()
    dim_natureza = pd.DataFrame({'descricao': naturezas_unicas})
    dim_natureza['id_natureza'] = dim_natureza.index + 1
    
    def categorizar_natureza(desc):
        desc = str(desc).upper()
        if 'AMEACA' in desc: return 'Ameaça'
        if 'LESAO' in desc or 'VIAS DE FATO' in desc or 'AGRESSAO' in desc: return 'Agressão Física'
        if 'ESTUPRO' in desc or 'SEXUAL' in desc: return 'Crime Sexual'
        if 'DESCUMPRIMENTO' in desc: return 'Quebra de Medida'
        if 'HOMICIDIO' in desc or 'FEMINICIDIO' in desc: return 'Crime Letal'
        return 'Outros'
        
    dim_natureza['categoria'] = dim_natureza['descricao'].apply(categorizar_natureza)
    
    fato_ocorrencia = df.copy()
    fato_ocorrencia = fato_ocorrencia.merge(dim_natureza, left_on='natureza_delito', right_on='descricao', how='left')
    fato_ocorrencia = fato_ocorrencia.rename(columns={'municipio_cod': 'id_municipio'})
    fato_ocorrencia['data_fato'] = pd.to_datetime(fato_ocorrencia['data_fato'], dayfirst=True, errors='coerce')
    fato_ocorrencia['trimestre'] = fato_ocorrencia['data_fato'].dt.quarter
    
    colunas_fato = ['id_municipio', 'id_natureza', 'data_fato', 'mes', 'trimestre', 'ano', 'tentado_consumado', 'qtde_vitimas']
    fato_ocorrencia = fato_ocorrencia[colunas_fato].dropna(subset=['id_municipio', 'id_natureza'])
    
    fato_ocorrencia.index += 1
    fato_ocorrencia.index.name = 'id_ocorrencia'
    fato_ocorrencia = fato_ocorrencia.reset_index()
    
    return dim_municipio, dim_natureza, fato_ocorrencia

def persistir_sqlite(dim_municipio, dim_natureza, fato_ocorrencia, db_path: Path):
    engine = sqla.create_engine(f"sqlite:///{db_path}")
    
    with engine.begin() as conn:
        dim_municipio.to_sql('Dim_Municipio', conn, if_exists='replace', index=False)
        dim_natureza.to_sql('Dim_Natureza', conn, if_exists='replace', index=False)
        fato_ocorrencia.to_sql('Fato_Ocorrencia', conn, if_exists='replace', index=False)
        
    return engine

def pipeline_etl(data_dir: Path, db_path: Path):
    df_bruto = carregar_dados_brutos(data_dir)
    dim_mun, dim_nat, fato_oc = processar_modelo_relacional(df_bruto)
    engine = persistir_sqlite(dim_mun, dim_nat, fato_oc, db_path)
    return engine