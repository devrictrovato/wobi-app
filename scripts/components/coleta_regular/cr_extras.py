import streamlit as st

from scripts.events import clear_filters, set_no_link, set_qtd_alert


def cr_qtd_alert():
    """
    Marca as duplicatas encontradas na base de dados.
    """
    if st.button("🧮 Qtd Exposta", disabled=False):
        with st.spinner("Processando..."):
            set_qtd_alert('Quantas_pecas_do_produto_estao_expostas')
            st.success("Alertas de quantidade marcadas!")

def cr_no_media():
    """
    Marca as notas fiscais sem link para imagem.
    """
    if st.button('🔗 NoMedia', disabled=False):
        with st.spinner("Processando..."):
            set_no_link()
            st.success("NoMedia Marcados!")

def cr_clear_cache():
    """
    Limpa os filtros e reseta as variáveis.
    """
    if st.button('♻️ Limpar Cache', disabled=True):
        with st.spinner("Processando..."):
            clear_filters()
            st.success("Cache Liberado!")