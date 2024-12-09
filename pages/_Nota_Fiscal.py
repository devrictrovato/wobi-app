# Bibliotecas
import streamlit as st
import pandas as pd

from scripts.components import footer, nf_links, nf_photo, nf_status
from scripts.data import get_current_status, set_image_index
from scripts.desc import display_nf_details

# Configuração de Página
st.set_page_config(page_title="Nota Fiscal", page_icon="🧾", layout='wide')

if st.session_state.data is not None:
    # Filtro de LINK1, LINK2, LINK3
    links = ["Foto_da_NF", "Foto_da_NF_2", "Foto_da_NF_3"]
    foto_coluna = st.sidebar.selectbox("Selecione uma Foto:", links)
    image_paths = st.session_state.data[foto_coluna].to_list()  # Filtra valores não nulos

    # st.session_state.data['Duplicidade'] = st.session_state.data['CNPJ'] + st.session_state.data['Itens Descrição'] + st.session_state.data['Numero_da_NF']

    # Navegação e Exibição
    if image_paths:
        # Lista de Links das fotos
        image_index = nf_links(image_paths)
        set_image_index(image_index)

        # Foto Atual
        current_image = image_paths[image_index]
        if pd.isna(current_image):
            # Verificando caso não haja nenhuma foto
            st.error('Foto não encontrada! (selecione outra foto)')
        else:
            # Apresentando as fotos
            nf_photo(current_image, image_paths)

            # Exibir Informações da NF
            display_nf_details(st.session_state.data.iloc[image_index])

            # Atualizar o status da imagem atual no selectbox
            current_status = get_current_status(st.session_state.data, image_index)

            # Alterar STATUS
            nf_status(image_index, current_status)
    else:
        st.error("Nenhuma foto encontrada!")
else:
    st.error('Essa base de dados não é válida!')

footer()