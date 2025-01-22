# Bibliotecas
import streamlit as st
import pandas as pd

from scripts.components.builders import display_note, image_index_input, photo
from scripts.components.nota_fiscal.nf_desc import display_nf_details, display_nf_ids
from scripts.data.data import session_vars
from scripts.events import get_current_status, set_status
from scripts.utils import footer

# Configuração da página
st.set_page_config(page_title="Nota Fiscal", page_icon="🧾", layout='wide')
session_vars()

# Obter dados filtrados da sessão
df = st.session_state.filtred_data

if st.button('⟳ Resetar o índice'):
    st.session_state.image_index = 0

# Exibir balões se o processamento estiver finalizado
if st.session_state.finished:
    st.balloons()
    st.session_state.finished = False

# Verificar se há dados válidos e se o tipo de dado é 'NF'
if (df is not None) and (st.session_state.type_data == 'NF'):
    # Filtro de Foto da Nota Fiscal
    links = ["Foto_da_NF", "Foto_da_NF_2", "Foto_da_NF_3"]
    foto_coluna = st.sidebar.selectbox("Selecione uma Foto:", links)
    image_paths = df[foto_coluna].to_list()  # Filtra valores não nulos

    if st.session_state.image_index > len(image_paths):
        st.session_state.image_index = 0

    # Exibição das fotos, se existirem
    if image_paths:
        # Exibir as fotos disponíveis
        image_index_input(image_paths)

        # Foto atual a ser exibida
        current_image = image_paths[st.session_state.image_index]

        if pd.isna(current_image):
            st.error('Foto não encontrada! (selecione outra foto)')
        else:
            # Exibir a foto atual e informações
            photo(current_image, image_paths)
            display_nf_details(df.iloc[st.session_state.image_index])
            display_nf_ids()

            # Obter e exibir o status atual da foto
            current_status = get_current_status(df, st.session_state.image_index)
            options = [
                'PENDENTE', 'APROVADO', 
                'VALOR DIVERGENTE', 'DUPLICIDADE', 
                'AUSENCIA DE DADOS', 'NUMERO DA NF DIVERGENTE', 
                'SKU DIVERGENTE', 'DATA DIVERGENTE',
                'FILIAL DIVERGENTE', 'QUANTIDADE DIVERGENTE', 
                'ILEGÍVEL', 'SEM LINK'
            ]
            display_note(
                df, 'Status', st.session_state.image_index, current_status,
                sorted(options), 'status', set_status
            )
    else:
        st.error("Nenhuma foto encontrada!")
else:
    st.error('Essa base de dados não é válida!')

# Exibir o rodapé
footer()
