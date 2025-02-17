import streamlit as st

from scripts.events import clear_filters, set_duplicates, set_no_link, set_wrong_date


def nf_duplicates():
    """
    Marca as duplicatas encontradas na base de dados.
    """
    if st.button("🚀 Duplicatas", disabled=False):
        with st.spinner("Processando..."):
            set_duplicates('Duplicidade')
            st.success("Duplicidades Marcadas!")

def nf_wrong_date():
    """
    Marca as datas divergentes.
    """
    if st.button('📅 Datas', disabled=False):
        with st.spinner("Processando..."):
            set_wrong_date('Data_da_venda')
            st.success("Datas Divergentes Marcadas!")

def nf_no_media():
    """
    Marca as notas fiscais sem link para imagem.
    """
    if st.button('🔗 NoMedia', disabled=False):
        with st.spinner("Processando..."):
            set_no_link()
            st.success("NoMedia Marcados!")

def nf_clear_cache():
    """
    Limpa os filtros e reseta as variáveis.
    """
    if st.button('♻️ Limpar Cache', disabled=True):
        with st.spinner("Processando..."):
            clear_filters()
            st.success("Cache Liberado!")
