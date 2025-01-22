import streamlit as st
import pandas as pd
from scripts.components.nota_fiscal.nf_filter import nf_filter
from scripts.components.coleta_regular.cr_filter import cr_filter
from scripts.data.data import save_filter_state
from scripts.events import clear_filters

# Função para exibir filtros
def display_filters(df: pd.DataFrame):
    try:
        if st.session_state.type_data == 'NF':
            df = nf_filter(df)
        elif st.session_state.type_data == 'CR':
            df = cr_filter(df)
    except Exception as e:
        st.error(f'Erro na filtragem de dados! (Tente outro filtro)')
        print(e)
        clear_filters()

# Função genérica para filtro por data
def filter_by_date(df, column):
    if column not in df.columns:
        st.warning(f'Coluna {column} não encontrada na base de dados.')
        return df

    date_min = df[column].min()
    date_max = df[column].max()

    data_inicio, data_fim = st.sidebar.date_input(
        f'Selecione o intervalo de {column}',
        value=(st.session_state.filters.get(f'{column}_inicio', date_min), st.session_state.filters.get(f'{column}_fim', date_max)),
        min_value=date_min,
        max_value=date_max,
        key=f'{column}_intervalo'
    )
    save_filter_state(f'{column}_inicio', data_inicio)
    save_filter_state(f'{column}_fim', data_fim)
    return df[(df[column] >= pd.to_datetime(data_inicio)) & (df[column] <= pd.to_datetime(data_fim))]

# Função genérica para filtro por múltiplos valores (multiselect)
def filter_by_multiselect(df, columns):
    for coluna, label in columns.items():
        if coluna not in df.columns:
            st.warning(f'Coluna {coluna} não encontrada na base de dados.')
            continue

        valores_unicos = sorted(df[coluna].dropna().unique())
        valores_selecionados = st.sidebar.multiselect(
            label,
            valores_unicos,
            default=st.session_state.filters.get(coluna, []),
            key=coluna
        )
        save_filter_state(coluna, valores_selecionados)
        if valores_selecionados:
            df = df[df[coluna].isin(valores_selecionados)]
    return df

# Função genérica para filtro por slider (intervalos numéricos)
def filter_by_slider(df, column, label):
    if column not in df.columns:
        st.warning(f'Coluna {column} não encontrada na base de dados.')
        return df

    min_value, max_value = df[column].min(), df[column].max()
    selected_range = st.sidebar.slider(
        label,
        min_value=int(min_value),
        max_value=int(max_value),
        value=st.session_state.filters.get(column, (int(min_value), int(max_value))),
        key=column
    )
    save_filter_state(column, selected_range)
    if selected_range:
        df = df[(df[column] >= selected_range[0]) & (df[column] <= selected_range[1])]
    return df

# Função para aplicar filtro por mês
def filter_by_month(df, column):
    if column not in df.columns:
        st.warning(f'Coluna {column} não encontrada na base de dados.')
        return df

    meses_unicos = sorted(df[column].unique())
    mes_selecionado = st.sidebar.selectbox(
        f'Selecione o mês da venda',
        options=meses_unicos,
        index=0 if column not in st.session_state.filters else meses_unicos.index(st.session_state.filters[column]),
        key=column
    )
    save_filter_state(f'{column}', mes_selecionado)
    return df[df[column] == mes_selecionado]

# Função para aplicar filtro de pendentes
def filter_pending(df):
    if 'STATUS' not in df.columns:
        st.warning(f'Coluna STATUS não encontrada na base de dados.')
        return df

    verificar_pendentes = st.sidebar.checkbox(
        'Pendentes',
        value=st.session_state.filters.get('verificar_pendentes', False),
        key='verificar_pendentes'
    )
    save_filter_state('verificar_pendentes', verificar_pendentes)
    if verificar_pendentes:
        df = df[df['STATUS'] == 'PENDENTE']
    return df
