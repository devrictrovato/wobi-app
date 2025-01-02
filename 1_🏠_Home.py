# Bibliotecas
import streamlit as st

from scripts.components.builders import exports, footer, nf_explain, nf_show, login
from scripts.data.data import load_data, session_vars
from scripts.components.filters import display_filters
from scripts.events import clear_cache, clear_filters

# Configurações de página
st.set_page_config(page_title="W.O.B.I", page_icon="🏠")
st.title("⚡ W.O.B.I ⚡")
session_vars()

# wobi_acess = login()
wobi_acess = True

if wobi_acess:
    nf_explain()

    # Interface para upload do arquivo
    uploaded_file = st.file_uploader("Carregue um arquivo Excel (.csv, .xlsx ou .xls)", type=["xlsx", "xls", "csv"])

    # Verificar se o arquivo foi carregado
    if uploaded_file:
        try:
            df = load_data(uploaded_file)
            st.session_state.data = df
            st.session_state.filtred_data = df.copy()
            clear_filters()
            st.success("Arquivo carregado com sucesso!")
        except ValueError as e:
            st.error(f"Erro no formato do arquivo: {e}")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")

    # Verificar se há dados no session_state
    if st.session_state.data is not None:
        display_filters(st.session_state.data)
        nf_show()
        exports()
    else:
        st.info("Por favor, carregue um arquivo Excel para começar.")
else:
    clear_cache()

footer()