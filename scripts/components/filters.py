import streamlit as st
import pandas as pd
from scripts.events import clear_filters, set_duplicates

# Função para salvar os valores dos filtros no estado da sessão
def save_filter_state(key, value):
    st.session_state.filters[key] = value

# Função para filtrar dados
def filter_data(data, coluna_filtro, valor_filtro):
    """Filtrar os dados e salvar no estado da sessão."""
    save_filter_state(coluna_filtro, valor_filtro)
    return data[data[coluna_filtro].isin(valor_filtro)]

# Função para definir o tipo de dado com base nas colunas do DataFrame
def define_type_data(df):
    """Definir o tipo de dados com base nas colunas."""
    if 'STATUS' in df.columns: 
        st.session_state.type_data = 'NF'
    elif 'ERRO' in df.columns: 
        st.session_state.type_data = 'CR'

def boxplot_df(df: pd.DataFrame, group, aggs):
    # Calcular agregações
    agg_df = df.groupby(group)['preço'].agg(aggs)
    agg_df['preco_minimo'] = agg_df['mean'] - agg_df['std']
    agg_df['preco_maximo'] = agg_df['mean'] + agg_df['std']
    
    # Fazer o merge para associar as margens ao DataFrame original, preservando o índice
    merged_df = df.merge(agg_df, on=group, how='left', left_index=False, right_index=False)
    
    # Adicionar coluna de verificação de margem
    def verifica_margem(row):
        if pd.isna(row['preco_minimo']) or pd.isna(row['preco_maximo']):
            return None
        return row['preco_minimo'] <= row['preço'] <= row['preco_maximo']
    
    merged_df['fora_intervalo'] = merged_df.apply(verifica_margem, axis=1)
    
    # Garantir que o índice original de df seja preservado após as operações
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
        print(e)
        clear_filters()

# Função de filtro para Coleta Regular
def cr_filter(df):
    """Aplicar filtros para os dados de Coleta Regular."""
    df = filter_by_date(df, 'data')
    df = filter_by_multiselect(df, {
        'nome_promotor': 'Selecione os Promotores',
        'e_supervisor': 'Selecione os Supervisores',
        # 'rede': 'Selecione as Redes',
        'bandeira': 'Selecione as Bandeiras',
        'nome_loja': 'Selecione as Lojas',
        'regiao': 'Selecione as Regiões',
        # 'sku': 'Selecione os SKUs',
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
    """Aplicar filtros para os dados de Nota Fiscal."""
    df = filter_by_month(df, 'Mes_da_venda')
    df = filter_by_date(df, 'Data Hora Tarefa')
    df = filter_by_multiselect(df, {
        'Região': 'Região',
        'Bandeira': 'Bandeira',
        'BU': 'BU',
    })
    
    # Filtro para duplicidades e pendentes
    df = filter_duplicates(df)
    df = filter_pending(df)
    
    # Limpeza de NaN e filtro por Preço Unitário
    df = df.dropna(subset=['Preco_unitario_da_venda'])
    df = filter_by_slider(df, 'Preco_unitario_da_venda', 'Selecione o intervalo de Preço Unitário da Venda')
    
    st.session_state.filtred_data = df
    return df

# Função genérica para filtro por data
def filter_by_date(df, column):
    """Aplicar filtro por data em um DataFrame."""
    date_min = df[column].min()
    date_max = df[column].max()

    data_selecionada = st.sidebar.date_input(
        f'Selecione uma {column} de partida',
        value=st.session_state.filters.get(f'{column}_inicio', date_min),
        min_value=date_min,
        max_value=date_max,
        key=f'{column}_inicio'
    )
    save_filter_state(f'{column}_inicio', data_selecionada)
    return df[df[column] >= pd.to_datetime(data_selecionada)]

# Função genérica para filtro por múltiplos valores (multiselect)
def filter_by_multiselect(df, columns):
    """Aplicar filtro por múltiplos valores em colunas específicas."""
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
    """Aplicar filtro por intervalo de valores em uma coluna numérica."""
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
    """Aplicar filtro por mês em uma coluna de DataFrame."""
    meses_unicos = sorted(df[column].unique())
    mes_selecionado = st.sidebar.selectbox(
        f'Selecione o mês da venda',
        options=meses_unicos,
        index=0 if column not in st.session_state.filters else meses_unicos.index(st.session_state.filters[column]),
        key=column
    )
    return df[df[column] == mes_selecionado]

# Função para aplicar filtro de duplicidade
def filter_range(df):
    """Aplicar filtro de ranges (checkbox)."""
    verificar_intervalo = st.sidebar.checkbox(
        'Fora do intervalo',
        key='verificar_intervalos'
    )
    if verificar_intervalo:
        df = df[df['fora_intervalo'] == False]
    return df

def filter_outliers(df, column):
    """Aplicar filtro de outliers (checkbox)."""
    verificar_outliers = st.sidebar.checkbox(
        'Outliers',
        key='verificar_outliers'
    )
    if verificar_outliers:
        # Calculando os quartis
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        # Definindo limites
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Filtrando valores dentro dos limites
        df = df[df[column] <= upper_bound]
    return df

def filter_ends_with(df):
    """Aplicar filtro de outliers (checkbox)."""
    # Slider para selecionar o intervalo de terminologia
    selected_ends_with = st.sidebar.slider(
        'Terminologia do preço',
        min_value=0,
        max_value=9,  # Incluindo o valor 9 para uma faixa de 0 a 9
        value=(0, 9),  # Intervalo inicial padrão
        key='termino_preço',
        step=1
    )
    
    # Se um intervalo for selecionado
    if selected_ends_with:
        i, j = selected_ends_with
        x = list(map(str, range(i, j + 1)))  # Converter números em string para comparar com o final do preço
        # Filtrando com base no último dígito da parte inteira do preço
        df = df[df['preço'].astype(str).str.split('.').str[0].str[-1].isin(x)]
    
    return df

# Função para aplicar filtro de duplicidade
def filter_duplicates(df):
    """Aplicar filtro de duplicidade (checkbox)."""
    verificar_duplicatas = st.sidebar.checkbox(
        'Duplicidade (1ª Ocorrência)',
        value=st.session_state.filters.get('verificar_duplicatas', False),
        key='verificar_duplicatas'
    )
    if verificar_duplicatas:
        df = set_duplicates(df, 'Duplicidade')
    return df

# Função para aplicar filtro de pendentes
def filter_pending(df):
    """Aplicar filtro de pendentes (checkbox)."""
    verificar_pendentes = st.sidebar.checkbox(
        'Pendentes',
        value=st.session_state.filters.get('verificar_pendentes', False),
        key='verificar_pendentes'
    )
    if verificar_pendentes:
        df = df[df['STATUS'] == 'PENDENTE']
    return df
