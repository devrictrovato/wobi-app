from PIL import Image
import requests
from io import BytesIO
import streamlit as st

def load_image(url):
    """Carregar uma imagem de uma URL."""
    response = requests.get(url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    image.resize((800, 600))
    return image

def transform_image(image, rotation_angle):
    """Aplicar transformações na imagem."""
    return image.rotate(rotation_angle, expand=True)

def opt_image():
    # Exibir os botões de rotação em uma linha
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Rotacionar -90°"):
            st.session_staterotation_angle = (st.session_state.get("rotation_angle", 0) - 90) % 360

    with col2:
        if st.button("Rotacionar +90°"):
            st.session_staterotation_angle = (st.session_state.get("rotation_angle", 0) + 90) % 360

    with col3:
        if st.button("Rotacionar -180°"):
            st.session_staterotation_angle = (st.session_state.get("rotation_angle", 0) - 180) % 360

    with col4:
        if st.button("Rotacionar +180°"):
            st.session_staterotation_angle = (st.session_state.get("rotation_angle", 0) + 180) % 360

