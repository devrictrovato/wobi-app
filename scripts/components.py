import streamlit as st

from scripts.data import set_status
from scripts.images import load_image, rotate_image

def nf_links(images):
    # Campo numérico para selecionar a imagem pelo índice
    image_index = st.number_input(
        "Navegar pelas imagens (índice da linha):",
        min_value=0,
        max_value=len(images) - 1,
        value=st.session_state.image_index,
        # key='image_index',
        step=1,
        format="%d",
    )
    return image_index

def nf_photo(current_image, image_paths):
    # Carregar a imagem atual
    foto_imagem = load_image(current_image)
    foto_atual = st.image(
        foto_imagem,
        caption=f"Foto {st.session_state.image_index + 1} / {len(image_paths)}",
        # width=1000,
        use_container_width=True,
    )
    rotate_image(foto_atual, foto_imagem)

def nf_status(image_index, current_status):
    status_options = sorted([
        'NENHUM', 'APROVADO',
        'VALOR DIVERGENTE', 'DUPLICIDADE', 
        'AUSENCIA DE DADOS', 'NUMERO DA NF DIVERGENTE', 
        'SKU DIVERGENTE', 'DATA DIVERGENTE', 
        'FILIAL DIVERGENTE', 'QUANTIDADE DIVERGENTE', 
        'ILEGÍVEL', 'SEM LINK'
    ])
    st.sidebar.selectbox(
        "Alterar Status:",
        options=status_options,
        key="status",
        on_change=lambda: set_status(
            st.session_state.data, image_index, st.session_state.status
        ),
        index=status_options.index(current_status) if current_status in status_options else 0,
    )

def footer():
    footer = """
    <style>
    footer {
        visibility: hidden;
    }

    .footer-container {
        width: 100%;
        text-align: center;
        margin-top: 50px;
        font-size: 14px;
        color: #6c757d;
        border-top: 1px solid #eaeaea;
        padding: 10px 0;
    }

    .footer-container a {
        color: #007bff;
        text-decoration: none;
    }

    .footer-container a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="footer-container">
        © 2024 W.O.B.I | Desenvolvido por <a href="https://github.com/devrictrovato" target="_blank">Ricardo Trovato</a>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)