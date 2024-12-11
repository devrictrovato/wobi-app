import streamlit as st
import pandas as pd

def filter_data(data, coluna_filtro, valor_filtro):
    # Filtrar os dados e salvar no estado da sessão
    return data[data[coluna_filtro].isin(valor_filtro)]

def display_filters(df):
    # Exibição de filtros

    # Filtro para a data da coleta
    data_inicio = st.sidebar.date_input('Selecione a data de início', min_value=df['Data Hora Tarefa'].min(), max_value=df['Data Hora Tarefa'].max())
    data_fim = st.sidebar.date_input('Selecione a data de fim', min_value=df['Data Hora Tarefa'].min(), max_value=df['Data Hora Tarefa'].max())
    if data_inicio and data_fim:
        df = df[(df['Data Hora Tarefa'] >= pd.to_datetime(data_inicio)) & (df['Data Hora Tarefa'] <= pd.to_datetime(data_fim))]

    # Filtro para UF, Cidade, Região, Bandeira, BU (multiselect)
    filtro_multiselect = {
        'UF': 'UF',
        'Cidade': 'Cidade',
        'Região': 'Região',
        'Bandeira': 'Bandeira',
        'BU': 'BU'
    }

    for col, label in filtro_multiselect.items():
        unique_values = df[col].unique()
        selected_values = st.sidebar.multiselect(f'Selecione valores para {label}', unique_values, default=[])
        if selected_values:
            df = filter_data(df, col, selected_values)

    # Filtro para Itens Descrição (multiselect)
    itens_descricoes = df['Itens Descrição'].unique()
    itens_selecionados = st.sidebar.multiselect('Selecione os Itens Descrição', itens_descricoes, default=[])
    if itens_selecionados:
        df = df[df['Itens Descrição'].isin(itens_selecionados)]

    # Filtro para Preço unitário da venda (slicer)
    preco_min, preco_max = float(df['Preco_unitario_da_venda'].min()), float(df['Preco_unitario_da_venda'].max())
    preco_selecionado = st.sidebar.slider('Selecione o intervalo de Preço Unitário da Venda', min_value=preco_min, max_value=preco_max, value=(preco_min, preco_max))
    if preco_selecionado:
        df = df[(df['Preco_unitario_da_venda'] >= preco_selecionado[0]) & (df['Preco_unitario_da_venda'] <= preco_selecionado[1])]

    st.session_state.filtered_data = df
    return df