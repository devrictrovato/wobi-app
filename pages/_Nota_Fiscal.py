# Bibliotecas
import streamlit as st
import pandas as pd

from scripts.components.builders import footer, nf_links, nf_photo, nf_status
from scripts.desc import display_nf_details
from scripts.events import get_current_status

# Configuração de Página
st.set_page_config(
    page_title="Nota Fiscal", page_icon="🧾", layout='wide',
)

# tipo_base = st.sidebar.selectbox('Selecione os dados:', ['Todos', 'Duplicidade'])

df = st.session_state.filtered_data

if st.session_state.finished:
    st.balloons()
    st.session_state.finished = False

if st.button('⟳ Resetar o indice'):
    st.session_state.image_index = 0

if df is not None:
    # Filtro de LINK1, LINK2, LINK3
    links = ["Foto_da_NF", "Foto_da_NF_2", "Foto_da_NF_3"]
    foto_coluna = st.sidebar.selectbox("Selecione uma Foto:", links)
    image_paths = df[foto_coluna].to_list()  # Filtra valores não nulos

    # Navegação e Exibição
    if image_paths:
        # Lista de Links das fotos
        nf_links(image_paths)

        # Foto Atual
        current_image = image_paths[st.session_state.image_index]

        if pd.isna(current_image):
            # Verificando caso não haja nenhuma foto
            st.error('Foto não encontrada! (selecione outra foto)')
        else:
            # Apresentando as fotos
            nf_photo(current_image, image_paths)

            # Exibir Informações da NF
            display_nf_details(df.iloc[st.session_state.image_index])

            # Atualizar o status da imagem atual no selectbox
            current_status = get_current_status(df, st.session_state.image_index)

            # Alterar STATUS
            nf_status(df, st.session_state.image_index, current_status)
    else:
        st.error("Nenhuma foto encontrada!")
else:
    st.error('Essa base de dados não é válida!')

footer()