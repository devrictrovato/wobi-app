import streamlit as st

from scripts.components.nota_fiscal.nf_extras import nf_clear_cache, nf_duplicates, nf_no_media, nf_wrong_date

def extra_options():
    """
    Exibe as opções extras de filtros para Notas Fiscais.
    """
    with st.expander('Opções extras'):
        if st.session_state.type_data == 'NF':
            col1, col2, col3, col4 = st.columns(4, vertical_alignment='center')
            with col1: nf_duplicates(st.session_state.data)
            with col2: nf_wrong_date(st.session_state.data)
            with col3: nf_no_media(st.session_state.data)
            with col4: nf_clear_cache()