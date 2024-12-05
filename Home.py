# Bibliotecas
import streamlit as st
import pandas as pd
from io import BytesIO

from scripts.data import filter_data

# Configurações de página
st.set_page_config(page_title="Home", page_icon="📂")
st.title("W.O.B.I")

# Funções
@st.cache_data
def load_data(file):
    """
    Função para carregar dados do Excel e armazená-los no cache.
    """
    if file.name.endswith('.csv'):
        df = pd.read_csv(file, sep=';', skiprows=1)
    else:
        df = pd.read_excel(file)
    if 'STATUS' in df.columns:
        df['STATUS'] = df['STATUS'].fillna('NENHUM')
    return df

def convert_to_excel(df):
    """
    Converte um DataFrame para um arquivo Excel em memória.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Validação")
    processed_data = output.getvalue()
    return processed_data

def convert_to_csv(df):
    """
    Converte um DataFrame para um arquivo CSV em memória.
    """
    return df.to_csv(index=False).encode("utf-8")

# Interface para upload do arquivo
uploaded_file = st.file_uploader("Carregue um arquivo Excel (.csv, .xlsx ou .xls)", type=["xlsx", "xls", "csv"])

# Verificar se o arquivo foi carregado
if uploaded_file:
    try:
        # Carregar os dados e salvar no session_state
        df = load_data(uploaded_file)
        st.session_state.data = df
        st.success("Arquivo carregado com sucesso!")
    except ValueError as e:
        st.error(f"Erro no formato do arquivo: {e}")
    except Exception as e:
        st.error(f"Erro inesperado: {e}")

# Verificar se há dados no session_state
if ("data" in st.session_state) and (st.session_state.data is not None):
    df = st.session_state.data

    # Exibir pré-visualização dos dados
    st.write('## Pré-visualização dos dados:')

    # coluna_filtro = st.sidebar.selectbox(
    #     "Selecione a coluna para filtrar:",
    #     options=df.columns,
    #     )
    # valor_filtro = st.sidebar.selectbox(
    #     "Qual valor para adicionar ao filtro:",
    #     options=df[coluna_filtro].unique(),
    # )
    # df = df[df[coluna_filtro] == valor_filtro]
    # st.session_state.data = df
    st.dataframe(df)
    
    # Botões de exportação
    st.markdown("### Exportar Dados:")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="⬇️ Exportar para Excel",
            data=convert_to_excel(df),
            file_name="VALIDAÇÃO.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col2:
        st.download_button(
            label="⬇️ Exportar para CSV",
            data=convert_to_csv(df),
            file_name="VALIDAÇÃO.csv",
            mime="text/csv"
        )
else:
    st.info("Por favor, carregue um arquivo Excel para começar.")
