from io import BytesIO
import pandas as pd
import streamlit as st

def session_vars():
    """
    Inicializa as variáveis de sessão necessárias.
    """
    if "data" not in st.session_state:
        st.session_state.data = None
    if "name" not in st.session_state:
        st.session_state.name = None
    if "filtred_data" not in st.session_state:
        st.session_state.filtred_data = None
    if "image_index" not in st.session_state:
        st.session_state.image_index = 0
    if "rotation_angle" not in st.session_state:
        st.session_state.rotation_angle = 0
    if "finished" not in st.session_state:
        st.session_state.finished = 0
    if 'filters' not in st.session_state:
        st.session_state.filters = {}

@st.cache_data
def load_data(file):
    """
    Função para carregar dados do Excel e armazená-los no cache.
    """
    if file.name.endswith('.csv'):
        df = pd.read_csv(file, sep=';', skiprows=1, converters=None)
    else:
        df = pd.read_excel(file, converters=None)
    if 'STATUS' in df.columns:
        df['STATUS'] = df['STATUS'].fillna('PENDENTE')
        df['CNPJ'] = df['CNPJ'].astype(str)
        df['Filial'] = df['Filial'].astype(str)
        df['Numero_da_NF'] = df['Numero_da_NF'].astype(str)
        df['Data_da_venda'] = pd.to_datetime(df['Data_da_venda'])
        df['Data_da_venda'] = pd.to_datetime(df['Data_da_venda'], format='%d/%m/%y')
        df['Mes_da_venda'] = df['Data_da_venda'].dt.month_name()
        month = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
            'April': 'Abril', 'May': 'Maio', 'June': 'Junho', 'July': 'Julho',
            'August': 'Agosto', 'September': 'Setembro', 'October': 'Outubro',
            'November': 'Novembro', 'December': 'Dezembro'
        }
        df['Mes_da_venda'] = df['Mes_da_venda'].map(month)
        df['Duplicidade'] = df['CNPJ'].astype(str) + df['Itens Descrição'].astype(str) + df['Numero_da_NF'].astype(str)
        df['Quem Validou?'] = None # Responsável pela validação
    return df

def convert_to_excel(df):
    """
    Converte um DataFrame para um arquivo Excel em memória.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Validação NF")
    processed_data = output.getvalue()
    return processed_data

def convert_to_csv(df):
    """
    Converte um DataFrame para um arquivo CSV em memória.
    """
    return df.to_csv(index=False).encode("utf-8")
