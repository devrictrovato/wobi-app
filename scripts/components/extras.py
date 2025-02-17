import streamlit as st

from scripts.components.nota_fiscal.nf_extras import nf_clear_cache, nf_duplicates, nf_no_media, nf_wrong_date
from scripts.components.coleta_regular.cr_extras import cr_clear_cache, cr_no_media, cr_qtd_alert

def extra_options():
    """
    Exibe as opções extras de filtros para Notas Fiscais.
    """
    with st.expander('Opções extras'):
        if st.session_state.type_data == 'NF':
            col1, col2, col3, col4 = st.columns(4, vertical_alignment='center')
            with col1: nf_duplicates()
            with col2: nf_wrong_date()
            with col3: nf_no_media()
            with col4: nf_clear_cache()
        elif st.session_state.type_data == 'CR':
            col1, col2, col3, col4 = st.columns(4, vertical_alignment='center')
            with col1: cr_qtd_alert()
            with col3: cr_no_media()
            with col4: cr_clear_cache()