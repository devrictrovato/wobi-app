import streamlit as st
import pandas as pd
from scripts.events import clear_filters, set_duplicates

def filter_data(data, coluna_filtro, valor_filtro):
    # Filtrar os dados e salvar no estado da sessão
    return data[data[coluna_filtro].isin(valor_filtro)]

def filters_sessions():
    # Função para atualizar os filtros na sessão
    st.session_state.filters['Mes_da_venda'] = st.session_state.get('mes_venda_inicio', None)
    st.session_state.filters['data_inicio'] = st.session_state.get('data_inicio', None)
    st.session_state.filters['verificar_duplicatas'] = st.session_state.get('verificar_duplicatas', False)
    st.session_state.filters['verificar_pendentes'] = st.session_state.get('verificar_pendentes', False)
    st.session_state.filters['preco_selecionado'] = st.session_state.get('preco_selecionado', (0, 0))
    for col in ['UF', 'Cidade', 'Região', 'Bandeira', 'BU']:
        st.session_state.filters[col] = st.session_state.get(col, [])

def display_filters(df: pd.DataFrame):
    try:
        # Preservar estado do filtro para o mês
        meses_unicos = sorted(df['Mes_da_venda'].unique())
        mes_selecionado = st.sidebar.selectbox(
            'Selecione o mês da venda',
            options=meses_unicos,
            index=0 if 'Mes_da_venda' not in st.session_state.filters else meses_unicos.index(st.session_state.filters['Mes_da_venda']),
            key='mes_venda_inicio',
            on_change=filters_sessions,
        )
        df = df[df['Mes_da_venda'] == mes_selecionado]

        # Preservar estado do filtro para as datas de coleta
        data_coleta = st.sidebar.date_input(
            'Selecione a data da coleta',
            value=st.session_state.filters.get('data_inicio', df['Data Hora Tarefa'].min()),
            min_value=df['Data Hora Tarefa'].min(),
            max_value=df['Data Hora Tarefa'].max(),
            key='data_inicio',
            on_change=filters_sessions,
        )
        df = df[(df['Data Hora Tarefa'] >= pd.to_datetime(data_coleta))]

        # Filtro para UF, Cidade, Região, Bandeira, BU (multiselect)
        filtro_multiselect = {
            'Região': 'Região',
            'Bandeira': 'Bandeira',
            'BU': 'BU',
        }

        for col, label in filtro_multiselect.items():
            unique_values = sorted(df[col].dropna().unique())
            selected_values = st.sidebar.multiselect(
                f'Selecione valores para {label}',
                unique_values,
                default=st.session_state.filters.get(col, []),
                key=col,
                on_change=filters_sessions,
            )
            st.session_state.filters[col] = selected_values
            if selected_values:
                df = filter_data(df, col, selected_values)

        # Filtro para Duplicidade (checkbox)
        verificar_duplicatas = st.sidebar.checkbox(
            'Duplicidade (1ª Ocorrência)',
            value=st.session_state.filters.get('verificar_duplicatas', False),
            key='verificar_duplicatas',
            on_change=filters_sessions,
        )
        if verificar_duplicatas:
            df = set_duplicates(df, 'Duplicidade')

        # Filtro para Pendentes (checkbox)
        verificar_pendentes = st.sidebar.checkbox(
            'Pendentes',
            value=st.session_state.filters.get('verificar_pendentes', False),
            key='verificar_pendentes',
            on_change=filters_sessions,
        )
        if verificar_pendentes:
            df = df[df['STATUS'] == 'PENDENTE']

        # Limpeza de NaN em Preço Unitário
        df = df.dropna(subset=['Preco_unitario_da_venda'])

        # Filtro para Preço unitário da venda (slider)
        if not df.empty:
            preco_min, preco_max = df['Preco_unitario_da_venda'].min(), df['Preco_unitario_da_venda'].max()
            preco_selecionado = st.sidebar.slider(
                'Selecione o intervalo de Preço Unitário da Venda',
                min_value=float(preco_min),
                max_value=float(preco_max),
                value=st.session_state.filters.get('preco_selecionado', (float(preco_min), float(preco_max))),
                key='preco_selecionado',
                on_change=filters_sessions,
            )
            if preco_selecionado:
                df = df[(df['Preco_unitario_da_venda'] >= preco_selecionado[0]) & 
                        (df['Preco_unitario_da_venda'] <= preco_selecionado[1])]

    except Exception as e:
        st.error(f'Erro na filtragem de dados! (Tente outro filtro) - {str(e)}')
        clear_filters()
    
    st.session_state.filtred_data = df
    return df
