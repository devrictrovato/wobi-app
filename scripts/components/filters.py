import streamlit as st
import pandas as pd
from scripts.events import clear_filters, set_duplicates

# Função para salvar os valores dos filtros no estado da sessão
def save_filter_state(key, value):
    st.session_state.filters[key] = value

# Função para filtrar dados
def filter_data(data, coluna_filtro, valor_filtro):
    save_filter_state(coluna_filtro, valor_filtro)
    return data[data[coluna_filtro].isin(valor_filtro)]

# Função para definir o tipo de dado com base nas colunas do DataFrame
def define_type_data(df):
    if 'STATUS' in df.columns: 
        st.session_state.type_data = 'NF'
    elif 'ERRO' in df.columns: 
        st.session_state.type_data = 'CR'

def boxplot_df(df: pd.DataFrame, group, aggs):
    agg_df = df.groupby(group)['preço'].agg(aggs)
    agg_df['preco_minimo'] = agg_df['mean'] - agg_df['std']
    agg_df['preco_maximo'] = agg_df['mean'] + agg_df['std']
    merged_df = df.merge(agg_df, on=group, how='left', left_index=False, right_index=False)

    def verifica_margem(row):
        if pd.isna(row['preco_minimo']) or pd.isna(row['preco_maximo']):
            return None
        return row['preco_minimo'] <= row['preço'] <= row['preco_maximo']

    merged_df['fora_intervalo'] = merged_df.apply(verifica_margem, axis=1)
    merged_df = merged_df.set_index(df.index)

    return merged_df

# Função para exibir filtros
def display_filters(df: pd.DataFrame):
    try:
        if st.session_state.type_data == 'NF':
            df = nf_filter(df)
        elif st.session_state.type_data == 'CR':
            df = cr_filter(df)
    except Exception as e:
        st.error(f'Erro na filtragem de dados! (Tente outro filtro)')
        raise e
        print(e)
        clear_filters()

# Função de filtro para Coleta Regular
def cr_filter(df):
    df = filter_by_date(df, 'data')
    df = filter_by_multiselect(df, {
        'nome_promotor': 'Selecione os Promotores',
        'e_supervisor': 'Selecione os Supervisores',
        'bandeira': 'Selecione as Bandeiras',
        'nome_loja': 'Selecione as Lojas',
        'regiao': 'Selecione as Regiões',
        'marca': 'Selecione as Marcas',
        'tecnologia': 'Selecione as Tecnologias',
        'ALERTAS DE VALIDAÇÃO': 'Selecione os Alertas de Validação',
    })

    df = boxplot_df(df, ['marca', 'tecnologia', 'sku'], ['mean', 'std'])
    df = filter_range(df)
    df = filter_outliers(df, 'preço')
    df = filter_ends_with(df)
    df = filter_by_slider(df, 'qtd_exposta', 'Selecione o intervalo de Quantidade Exposta')
    df = filter_by_slider(df, 'preço', 'Selecione o intervalo de Preço')

    st.session_state.filtred_data = df
    return df

# Função de filtro para Nota Fiscal
def nf_filter(df):
    df = filter_by_month(df, 'Mes_da_venda')
    df = filter_by_date(df, 'Data Hora Tarefa')
    df = filter_by_multiselect(df, {
        'Região': 'Região',
        'Bandeira': 'Bandeira',
        'BU': 'BU',
    })

    df = filter_duplicates(df)
    df = filter_pending(df)
    df = df.dropna(subset=['Preco_unitario_da_venda'])
    df = filter_by_slider(df, 'Preco_unitario_da_venda', 'Selecione o intervalo de Preço Unitário da Venda')

    st.session_state.filtred_data = df
    return df

# Função genérica para filtro por data
def filter_by_date(df, column):
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
    if not df.empty and column in df.columns:
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
    meses_unicos = sorted(df[column].unique())
    mes_selecionado = st.sidebar.selectbox(
        f'Selecione o mês da venda',
        options=meses_unicos,
        index=0 if column not in st.session_state.filters else meses_unicos.index(st.session_state.filters[column]),
        key=column
    )
    save_filter_state(f'{column}', mes_selecionado)
    return df[df[column] == mes_selecionado]

# Função para aplicar filtro de ranges
def filter_range(df):
    verificar_intervalo = st.sidebar.checkbox(
        'Fora do intervalo',
        value=st.session_state.filters.get('verificar_intervalos', False),
        key='verificar_intervalos'
    )
    save_filter_state('verificar_intervalos', verificar_intervalo)
    if verificar_intervalo:
        df = df[df['fora_intervalo'] == False]
    return df

# Função para aplicar filtro de outliers
def filter_outliers(df, column):
    verificar_outliers = st.sidebar.checkbox(
        'Outliers',
        value=st.session_state.filters.get('verificar_outliers', False),
        key='verificar_outliers'
    )
    save_filter_state('verificar_outliers', verificar_outliers)
    if verificar_outliers:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[df[column] > upper_bound]
    return df

# Função para aplicar filtro de terminologia
def filter_ends_with(df):
    selected_ends_with = st.sidebar.slider(
        'Terminologia do preço',
        min_value=0,
        max_value=9,
        value=st.session_state.filters.get('termino_preço', (0, 9)),
        key='termino_preço',
        step=1
    )
    save_filter_state('termino_preço', selected_ends_with)
    if selected_ends_with:
        i, j = selected_ends_with
        x = list(map(str, range(i, j + 1)))
        df = df[df['preço'].astype(str).str.split('.').str[0].str[-1].isin(x)]
    return df

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

# Função para aplicar filtro de pendentes
def filter_pending(df):
    verificar_pendentes = st.sidebar.checkbox(
        'Pendentes',
        value=st.session_state.filters.get('verificar_pendentes', False),
        key='verificar_pendentes'
    )
    save_filter_state('verificar_pendentes', verificar_pendentes)
    if verificar_pendentes:
        df = df[df['STATUS'] == 'PENDENTE']
    return df
