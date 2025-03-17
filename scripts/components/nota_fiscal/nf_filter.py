import streamlit as st
import scripts.components.filters as filters
from scripts.data.data import save_filter_state
from scripts.events import set_duplicates

# Função para aplicar filtro de duplicidade
def filter_duplicates(df):
    verificar_duplicatas = st.sidebar.checkbox(
        'Duplicidade (1ª Ocorrência)',
        value=st.session_state.filters.get('verificar_duplicatas', False),
        key='verificar_duplicatas'
    )
    save_filter_state('verificar_duplicatas', verificar_duplicatas)
    if verificar_duplicatas:
        df = set_duplicates(df, 'Duplicidade')
    return df

# Função de filtro para Nota Fiscal
def nf_filter(df):
    # df = filters.filter_by_date(df, 'Data Hora Tarefa')
    # df = filters.filter_by_month(df, 'Mes_da_venda')
    df = filters.filter_by_multiselect(df, {
        'Região': 'Região',
        'Bandeira': 'Bandeira',
        'BU': 'BU',
    })

    df = filter_duplicates(df)
    df = filters.filter_pending(df)
    df = df.dropna(subset=['Preco_unitario_da_venda'])
    df = filters.filter_by_slider(df, 'Preco_unitario_da_venda', 'Selecione o intervalo de Preço Unitário da Venda')

    st.session_state.filtred_data = df
    return df