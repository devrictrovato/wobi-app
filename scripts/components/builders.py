import streamlit as st

from scripts.events import set_image_index
from scripts.components.images import load_image, rotate_image

def show_df():
    """
    Exibe os dados filtrados e originais.
    """

    st.subheader("Exibindo Dados Originais (Importados/Exportados)")
    st.dataframe(st.session_state.data)

    st.subheader("Dados Filtrados (Opicional)")
    st.dataframe(st.session_state.filtred_data)

def image_index_input(images):
    """
    Exibe a foto selecionada com um campo para definir o índice da imagem.
    """
    st.number_input(
        "Defina o índice da imagem:",
        value=st.session_state.image_index,
        min_value=0,
        max_value=len(images) - 1,
        step=1,
        key='temp_image_index',
        on_change=set_image_index,
    )

def photo(current_image, image_paths):
    """
    Carrega e exibe a foto com opção de zoom controlada por um checkbox.
    """

    # Carregar a imagem
    foto_imagem = load_image(current_image)

    # Determinar índice atual e total de imagens
    image_index = st.session_state.get("image_index", 0) + 1
    total_images = len(image_paths)
    caption_text = f"Foto {image_index} / {total_images}"

    # Mostrar imagem com ou sem zoom
    if st.session_state.toggle_zoom:
        from streamlit_image_zoom import image_zoom

        foto_atual = image_zoom(foto_imagem, mode='both', zoom_factor=8, size=(800, 800))
        # st.caption(caption_text)
    else:
        foto_atual = st.image(foto_imagem, caption=caption_text, use_container_width=True,)

    # Girar imagem se necessário
    rotate_image(foto_atual, foto_imagem)

def display_note(df, column, image_index, current_status, options, key, change_func, next_image=True):
    st.sidebar.selectbox(
        f"Alterar {column}:",
        options=options,
        key=key,
        on_change=lambda: change_func(df, image_index, st.session_state[key], next_image),
        index=options.index(current_status) if current_status in options else 0,
    )
