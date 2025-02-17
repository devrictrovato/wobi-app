# Bibliotecas
import streamlit as st
import warnings

# Importações locais
from scripts.acess import login
from scripts.components.builders import show_df
from scripts.components.extras import extra_options
from scripts.components.nota_fiscal.nf_desc import nf_explain
from scripts.data.data import define_type_data, load_data, session_vars
from scripts.components.filters import display_filters
from scripts.events import clear_cache, clear_filters
from scripts.utils import exports, footer

# Suprime todos os warnings
warnings.filterwarnings("ignore")

# Configurações de página
st.set_page_config(page_title="W.O.B.I", page_icon="🏠")
st.title("⚡ W.O.B.I ⚡")

# Simula o login (essa linha pode ser modificada para implementar o login real)
wobi_acess = True
file_loaded = False
# wobi_acess = login()

# Verifica acesso do usuário
if wobi_acess:
    session_vars() # Inicializa variáveis de sessão
    nf_explain()  # Explicação sobre o sistema

    # Interface para upload do arquivo
    uploaded_file = st.file_uploader("Carregue um arquivo Excel (.csv, .xlsx ou .xls)", type=["xlsx", "xls", "csv"])

    # if not file_loaded:
    #     sheet_name = st.text_input('Coloque o nome da aba do excel aqui:',)

    # Verifica se o arquivo foi carregado
    if uploaded_file:
        try:
            # Carrega os dados
            df = load_data(uploaded_file)
            st.session_state.data = df
            st.session_state.filtred_data = df.copy()
            file_loaded = True
            
            # Processa os dados
            define_type_data(df)
            clear_filters()
            st.success("Arquivo carregado com sucesso!")
        except ValueError as e:
            st.error(f"Erro no formato do arquivo: {e}")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")

    # Verifica se há dados carregados
    if st.session_state.data is not None:
        exports()  # Opções de exportação
        display_filters(st.session_state.data)
        # extra_options()
        show_df()  # Exibe o DataFrame
    else:
        st.info("Por favor, carregue um arquivo Excel para começar.")
else:
    clear_cache()  # Limpa cache se não autorizado

footer()  # Rodapé da aplicação
