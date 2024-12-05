# Bibliotecas
import streamlit as st
import pandas as pd

from scripts.data import load_data, update_status, session_vars, get_current_status
from scripts.images import load_image
from scripts.desc import format_cnpj, display_nf_details

# Configuração de Página
st.set_page_config(page_title="Nota Fiscal", page_icon="🧾", layout='wide')

# Carregar Dados e Inicializar Estado
load_data()

# Variaveis de sessão
session_vars()

if st.session_state.data is not None:
    # Filtro de LINK1, LINK2, LINK3
    links = ["Foto_da_NF", "Foto_da_NF_2", "Foto_da_NF_3"]
    foto_coluna = st.sidebar.selectbox("Selecione uma Foto:", links)
    image_paths = st.session_state.data[foto_coluna].to_list()  # Filtra valores não nulos

    # st.session_state.data['Duplicidade'] = st.session_state.data['CNPJ'] + st.session_state.data['Itens Descrição'] + st.session_state.data['Numero_da_NF']

    # Navegação e Exibição
    if image_paths:
        # Campo numérico para selecionar a imagem pelo índice
        image_index = st.number_input(
            "Navegar pelas imagens (índice da linha):",
            min_value=0,
            max_value=len(image_paths) - 1,
            value=st.session_state.image_index,
            step=1,
            format="%d",
        )
        st.session_state.image_index = image_index

        current_image = image_paths[image_index]
        if pd.isna(current_image):
            st.error('Foto não encontrada! (selecione outra foto)')
        else:
            # Carregar a imagem atual
            foto_atual = load_image(current_image)
            st.image(
                foto_atual,
                caption=f"Foto {image_index + 1} / {len(image_paths)}",
                # width=1000,
                use_container_width=True,
            )

            # Exibir Informações da NF
            nf_info = st.session_state.data.iloc[image_index]
            display_nf_details(nf_info, format_cnpj)

            # Atualizar o status da imagem atual no selectbox
            current_status = get_current_status(st.session_state.data, image_index)
            status_options = sorted([
                'NENHUM', 'APROVADO', 'VALOR DIVERGENTE', 'DUPLICIDADE',
                'AUSENCIA DE DADOS', 'NUMERO DA NF DIVERGENTE', 'SKU DIVERGENTE',
                'DATA DIVERGENTE', 'FILIAL DIVERGENTE', 'QUANTIDADE DIVERGENTE', 'ILEGÍVEL', 'SEM LINK'
            ])

            # Alterar STATUS
            st.sidebar.selectbox(
                "Alterar Status:",
                options=status_options,
                key="status",
                index=status_options.index(current_status) if current_status in status_options else 0,
                on_change=lambda: update_status(st.session_state.data, image_index, st.session_state.status)
            )
    else:
        st.error("Nenhuma foto encontrada!")
else:
    st.error('Essa base de dados não é válida!')