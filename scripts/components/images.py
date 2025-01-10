from PIL import Image
import requests
from io import BytesIO
import streamlit as st

# Função para carregar imagem de uma URL
def load_image(url):
    """Carregar uma imagem de uma URL."""
    response = requests.get(url)
    response.raise_for_status()  # Levanta um erro em caso de falha na requisição
    image = Image.open(BytesIO(response.content))
    return image

# Função para aplicar transformação (rotação) na imagem
def transform_image(image, rotation_angle):
    """Aplicar transformações na imagem (rotação)."""
    return image.rotate(rotation_angle, expand=True)

def reset_rotation_image():
    st.session_state.rotation_angle = 0

# Função para exibir botões de rotação
def rotate_image(foto, image):
    # Exibir os botões de rotação em uma linha
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Definir os ângulos de rotação, rótulos e ícones
    rotations = {
        "Rotate -90°": {"angle": -90, "icon": "↩️"},
        "Rotate +90°": {"angle": 90, "icon": "↪️"},
        "Rotate -180°": {"angle": -180, "icon": "🔄"},
        "Rotate +180°": {"angle": 180, "icon": "🔃"}
    }

    # Exibir os botões dinamicamente com ícones
    for i, (label, data) in enumerate(rotations.items()):
        with (col1, col2, col3, col4)[i]:
            if st.button(f"{data['icon']} {label}"):
                st.session_state.rotation_angle = (st.session_state.get("rotation_angle", 0) + data["angle"]) % 360
                imagem_rotated = transform_image(image, st.session_state.rotation_angle)
                # Mostrar imagem rotacionada
                foto.image(imagem_rotated)
    with col5:
        st.checkbox("🔍 Zoom", key="toggle_zoom", value=st.session_state.toggle_zoom, on_change=reset_rotation_image)
