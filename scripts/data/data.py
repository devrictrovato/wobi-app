import pandas as pd
import streamlit as st
from scripts.data.analytics import cr_val_alert
from scripts.events import clear_filters

def session_vars():
    """
    Inicializa as variáveis de sessão necessárias.
    """
    session_defaults = {
        "data": None,
        "name": None,
        "filtred_data": None,
        "image_index": 0,
        "rotation_angle": 0,
        "finished": 0,
        "filters": {},
        "type_data": None,
        "toggle_zoom": False,
    }
    # Define variáveis no session_state se não existirem
    for key, default in session_defaults.items():
        st.session_state.setdefault(key, default)

# Função para salvar os valores dos filtros no estado da sessão
def save_filter_state(key, value):
    st.session_state.filters[key] = value

# Função para filtrar dados
def filter_data(data, coluna_filtro, valor_filtro):
    save_filter_state(coluna_filtro, valor_filtro)
    return data[data[coluna_filtro].isin(valor_filtro)]

# Função para definir o tipo de dado com base nas colunas do DataFrame
def define_type_data(df):
    if 'STATUS' in df.columns: 
        st.session_state.type_data = 'NF'
    elif 'ERRO' in df.columns: 
        st.session_state.type_data = 'CR'

@st.cache_data(max_entries=10, show_spinner=False)
def load_data(file):
    """
    Carrega dados do Excel/CSV e realiza pré-processamento.
    O resultado é armazenado em cache para reutilização.
    """
    clear_filters()

    try:
        # Carregar dados dependendo da extensão do arquivo
        if file.name.endswith('.csv'):
            chunks = pd.read_csv(file, sep=';', skiprows=1, low_memory=False, chunksize=10000)
            df = pd.concat(chunks, ignore_index=True)  # Concatena os chunks em um único DataFrame
        else:
            df = pd.read_excel(file, engine='openpyxl', converters=None)
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

    # Otimização de tipos de dados
    optimize_column_types(df)

    # Processamento de dados específicos
    if 'Foto_da_NF' in df.columns:
        df = process_nf_data(df)
    elif 'Tire_uma_foto_comprovando_o_preco_do_produto_etiqueta_ou_tela_do_sistema' in df.columns:
        df = process_cr_data(df)

    return df

def optimize_column_types(df):
    """
    Otimiza os tipos de dados de colunas específicas.
    """
    dtypes = {
        'CNPJ': 'string',
        'Filial': 'string',
        'Numero_da_NF': 'string',
    }
    for col, dtype in dtypes.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype)

def process_nf_data(df):
    """
    Processa dados específicos para o tipo NF (Nota Fiscal).
    """
    if 'STATUS' not in df.columns:
        df['STATUS'] = None
    df['STATUS'] = df['STATUS'].fillna('PENDENTE')
    df['Data_da_venda'] = pd.to_datetime(df.get('Data_da_venda'), errors='coerce', format='%d/%m/%y')
    df['Mes_da_venda'] = df['Data_da_venda'].dt.month_name()
    
    month_map = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
        'April': 'Abril', 'May': 'Maio', 'June': 'Junho', 'July': 'Julho',
        'August': 'Agosto', 'September': 'Setembro', 'October': 'Outubro',
        'November': 'Novembro', 'December': 'Dezembro'
    }
    df['Mes_da_venda'] = df['Mes_da_venda'].replace(month_map)
    df['Duplicidade'] = df['CNPJ'].fillna('') + df['Itens Descrição'].fillna('') + df['Numero_da_NF'].fillna('')
    df['Quem Validou?'] = None  # Inicializa coluna de validação

    st.session_state.type_data = 'NF'
    return df

def process_cr_data(df: pd.DataFrame):
    """
    Processa dados específicos para o tipo CR (Correção).
    """
    # Calcular a moda dos preços por SKU
    df['PREÇO MODA'] = df.groupby('Itens Descrição')['Qual_o_preco_deste_produto'].transform(lambda x: pd.Series.mode(x)[0])
    df['ALERTAS DE VALIDAÇÃO'] = df.apply(lambda row: cr_val_alert(row['Qual_o_preco_deste_produto'], row['PREÇO MODA']), axis=1)
    # Aplicar a função para gerar alertas de validação
    if 'CORREÇÃO' in df.columns:
        df['CORREÇÃO'] = df['CORREÇÃO'].astype(str)  # Convert to string
    if 'PREÇO MODA' in df.columns:
        df['PREÇO MODA'] = df['PREÇO MODA'].astype(str)  # Convert to string
    if 'ERRO' not in df.columns:
        df['ERRO'] = None
    df['ERRO'] = df['ERRO'].fillna('PENDENTE')

    st.session_state.type_data = 'CR'
    return df
