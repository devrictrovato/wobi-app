# Função de filtro para Coleta Regular
import streamlit as st
import scripts.components.filters as filters
from scripts.data.data import save_filter_state
from scripts.data.analytics import boxplot_df

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
        df = df[(df[column] < lower_bound) & (df[column] > upper_bound)]
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
        df = df[df['Qual_o_preco_deste_produto'].astype(str).str.split('.').str[0].str[-1].isin(x)]
    return df

def cr_filter(df):
    df = filters.filter_by_date(df, 'Data Hora Tarefa')
    df = filters.filter_by_multiselect(df, {
        # 'Tarefa ID para Integração': 'Selecione os IDs',
        'Local de Atendimento Descrição': 'Selecione as lojas',
        'Pessoa Nome': 'Selecione os promotores',
        'Itens Descrição': 'Selecione os SKUs',
        'Região': 'Selecione as regiões',
        'Marca': 'Selecione as marcas',
        'ALERTAS DE VALIDAÇÃO': 'Selecione os Alertas de Validação',
    })

    df = boxplot_df(df, ['Itens Descrição',], ['mean', 'std'])
    df = filter_range(df)
    df = filter_outliers(df, 'Qual_o_preco_deste_produto')
    df = filters.filter_by_slider(df, 'Quantas_pecas_do_produto_estao_expostas', 'Selecione o intervalo de Quantidade Exposta')
    df = filter_ends_with(df)
    # df = filter_by_slider(df, 'qtd_exposta', 'Selecione o intervalo de Quantidade Exposta')
    df = filters.filter_by_slider(df, 'Qual_o_preco_deste_produto', 'Selecione o intervalo de Preço')

    st.session_state.filtred_data = df
    return df