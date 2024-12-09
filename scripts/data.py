import streamlit as st

def session_vars():
    """Inicializa as variáveis de sessão necessárias."""
    if "data" not in st.session_state:
        st.session_state.data = None
    if "filtered_data" not in st.session_state:
        st.session_state.filtered_data = None
    if "image_index" not in st.session_state:
        st.session_state.image_index = 0  # Valor inicial
    if "rotation_angle" not in st.session_state:
        st.session_state.rotation_angle = 0

def set_image_index(image_index):
    st.session_state.image_index = image_index

def set_status(df, image_index, new_status):
    """Atualizar o STATUS da nota fiscal."""
    df.iloc[image_index, df.columns.get_loc("STATUS")] = new_status
    st.session_state.data = df
    st.session_state.image_index += 1
    st.session_state.status = get_current_status(df, image_index + 1)

def get_current_status(df, image_index):
    """Obtém o STATUS atual da imagem correspondente no DataFrame."""
    status = df.iloc[image_index, df.columns.get_loc("STATUS")]
    return status