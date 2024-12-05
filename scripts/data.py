import pandas as pd
import streamlit as st

def load_data():
    """Carregar e inicializar os dados no estado."""
    if "data" not in st.session_state:
        st.session_state.data = None
    return st.session_state.data

def session_vars():
    if "image_index" not in st.session_state:
        st.session_state.image_index = 0
    if "rotation_angle" not in st.session_state:
        st.session_state.rotation_angle = 0

def filter_data(data, coluna_filtro, valor_filtro):
    st.session_state.data = data[data[coluna_filtro] == valor_filtro]

def update_status(df, image_index, new_status):
    """Atualizar o STATUS da nota fiscal."""
    df.iloc[image_index, df.columns.get_loc("STATUS")] = new_status
    st.session_state.data = df

def get_current_status(df, image_index):
    """Obtém o STATUS atual da imagem correspondente no DataFrame."""
    status = df.iloc[image_index, df.columns.get_loc("STATUS")]
    return status