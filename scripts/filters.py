import streamlit as st

def filter_data(data, coluna_filtro, valor_filtro):
    # Filtrar os dados e salvar no estado da sessão
    return data[data[coluna_filtro].isin(valor_filtro)]

def display_filters(df, columns):
    for col in columns:
        # Obter valores únicos da coluna
        unique_values = df[col].unique()
        # Mostrar multiselect se houver até 5 valores únicos
        if len(unique_values) <= 5:
            selected_values = st.sidebar.multiselect(f'Selecione valores para {col}', unique_values)
            # Aplicar filtro se valores forem selecionados
            if selected_values:
                st.session_state.filtered_data = filter_data(df, col, selected_values)
