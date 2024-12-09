from PIL import Image
import requests
from io import BytesIO
import streamlit as st

def load_image(url):
    """Carregar uma imagem de uma URL."""
    response = requests.get(url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    return image

def transform_image(image, rotation_angle):
    """Aplicar transformações na imagem."""
    return image.rotate(rotation_angle, expand=True)

def rotate_image(foto, image):
    # Exibir os botões de rotação em uma linha
    col1, col2, col3, col4 = st.columns(4)
    
    # Definir os ângulos de rotação, rótulos e ícones
    rotations = {
        "Rotacionar -90°": {"angle": -90, "icon": "↩️"},
        "Rotacionar +90°": {"angle": 90, "icon": "↪️"},
        "Rotacionar -180°": {"angle": -180, "icon": "🔄"},
        "Rotacionar +180°": {"angle": 180, "icon": "🔃"}
    }
    
    # Exibir os botões dinamicamente com ícones
    for i, (label, data) in enumerate(rotations.items()):
        with (col1, col2, col3, col4)[i]:
            if st.button(f"{data['icon']} {label}"):
                st.session_state.rotation_angle = (st.session_state.get("rotation_angle", 0) + data["angle"]) % 360
                imagem_rotated = transform_image(image, st.session_state.rotation_angle)
                foto.image(imagem_rotated)
