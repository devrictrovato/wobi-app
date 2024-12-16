import streamlit as st
import pandas as pd
from scripts.events import set_image_index

def filter_data(data, coluna_filtro, valor_filtro):
    # Filtrar os dados e salvar no estado da sessão
    return data[data[coluna_filtro].isin(valor_filtro)]

def display_filters(df: pd.DataFrame):
    try:
        # Tratamento padrão para a coluna de Data_da_venda
        df['Data_da_venda'] = pd.to_datetime(df['Data_da_venda'], format='%d/%m/%y')

        # Criar uma nova coluna com o nome do mês
        df['Mes_da_venda'] = df['Data_da_venda'].dt.month_name()

        # Dicionário de mapeamento dos meses de inglês para português
        month = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
            'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
            'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
            'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
        }

        # Mapeando os nomes dos meses para o formato em português
        df['Mes_da_venda'] = df['Mes_da_venda'].map(month)

        # Inicializar estados de sessão
        if 'filters' not in st.session_state:
            st.session_state.filters = {}

        # Preservar estado do filtro para o mês
        meses_unicos = sorted(df['Mes_da_venda'].unique())
        mes_selecionado = st.sidebar.selectbox(
            'Selecione o mês da venda',
            options=meses_unicos,
            index=0 if 'Mes_da_venda' not in st.session_state.filters else meses_unicos.index(st.session_state.filters['Mes_da_venda'])
        )
        st.session_state.filters['Mes_da_venda'] = mes_selecionado
        df = df[df['Mes_da_venda'] == mes_selecionado]

        # Preservar estado do filtro para as datas de coleta
        data_inicio = st.sidebar.date_input(
            'Selecione a data de início da coleta',
            value=st.session_state.filters.get('data_inicio', df['Data Hora Tarefa'].min()),
            min_value=df['Data Hora Tarefa'].min(),
            max_value=df['Data Hora Tarefa'].max()
        )
        data_fim = st.sidebar.date_input(
            'Selecione a data de fim da coleta',
            value=st.session_state.filters.get('data_fim', df['Data Hora Tarefa'].max()),
            min_value=df['Data Hora Tarefa'].min(),
            max_value=df['Data Hora Tarefa'].max()
        )
        st.session_state.filters['data_inicio'] = data_inicio
        st.session_state.filters['data_fim'] = data_fim
        df = df[(df['Data Hora Tarefa'] >= pd.to_datetime(data_inicio)) & 
                (df['Data Hora Tarefa'] <= pd.to_datetime(data_fim))]

        # Filtro para UF, Cidade, Região, Bandeira, BU (multiselect)
        filtro_multiselect = {
            'UF': 'UF',
            'Cidade': 'Cidade',
            'Região': 'Região',
            'Bandeira': 'Bandeira',
            'BU': 'BU',
        }

        for col, label in filtro_multiselect.items():
            unique_values = sorted(df[col].unique())
            selected_values = st.sidebar.multiselect(
                f'Selecione valores para {label}',
                unique_values,
                default=st.session_state.filters.get(col, [])
            )
            st.session_state.filters[col] = selected_values
            if selected_values:
                df = filter_data(df, col, selected_values)

        # Pegar a primeira ocorrência das duplicidades
        verificar_pendentes = st.sidebar.checkbox(
            'Pendentes',
            value=st.session_state.filters.get('verificar_pendentes', False)
        )
        st.session_state.filters['verificar_pendentes'] = verificar_pendentes
        if verificar_pendentes:
            df = df[df['STATUS'] == 'PENDENTE']
            st.session_state.image_index = 0

        # verificar_duplicatas = st.sidebar.checkbox(
        #     'Duplicidade',
        #     value=st.session_state.filters.get('verificar_duplicatas', False)
        # )
        # st.session_state.filters['verificar_duplicatas'] = verificar_duplicatas
        # if verificar_duplicatas:
        #     df = set_duplicates(df, 'Duplicidade')

        # Filtro para Preço unitário da venda (slider)
        preco_min, preco_max = float(df['Preco_unitario_da_venda'].min()), float(df['Preco_unitario_da_venda'].max())
        preco_selecionado = st.sidebar.slider(
            'Selecione o intervalo de Preço Unitário da Venda',
            min_value=preco_min,
            max_value=preco_max,
            value=st.session_state.filters.get('preco_selecionado', (preco_min, preco_max))
        )
        st.session_state.filters['preco_selecionado'] = preco_selecionado
        if preco_selecionado:
            df = df[(df['Preco_unitario_da_venda'] >= preco_selecionado[0]) & 
                    (df['Preco_unitario_da_venda'] <= preco_selecionado[1])]

    except Exception as e:
        st.warning(f'Erro na filtragem de dados: {e}')
    st.session_state.filtered_data = df
    return df
