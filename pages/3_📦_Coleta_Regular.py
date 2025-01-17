# Bibliotecas
import streamlit as st
import pandas as pd

from scripts.components.builders import display_note, photo, image_index_input
from scripts.components.desc import display_cr_details
from scripts.data.data import session_vars
from scripts.events import get_current_errors, set_erros
from scripts.utils import footer

# Configuração da página
st.set_page_config(page_title="Coleta Regular", page_icon="📦", layout='wide')
session_vars()

# Obter dados filtrados da sessão
df = st.session_state.filtred_data

if st.button('⟳ Resetar o índice'):
    st.session_state.image_index = 0

# Exibir balões se o processamento estiver finalizado
if st.session_state.finished:
    st.balloons()
    st.session_state.finished = False

# Verificar se há dados válidos e se o tipo de dado é 'CR'
if (df is not None) and (st.session_state.type_data == 'CR'):
    # Filtro de Foto da Coleta Regular
    links = ["Tire_uma_foto_comprovando_o_preco_do_produto_etiqueta_ou_tela_do_sistema"]
    foto_coluna = st.sidebar.selectbox("Selecione uma Foto:", links)
    image_paths = df[foto_coluna].to_list()  # Filtra valores não nulos

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
            display_cr_details(df.iloc[st.session_state.image_index])

            # Obter e exibir os erros atuais da foto
            current_errors = get_current_errors(df, st.session_state.image_index)
            options = [
                'PENDENTE', 'SEM ERRO', 'ALERTA - FOTO ILEGÍVEL', 
                'ALERTA - NÚMERO DE EXPOSIÇÃO ZERADO',
                'ALERTA - PRODUTOS EXPOSTOS EM EXCESSO', 
                'VALIDADO - MODELO DA ETIQUETA DIFERENTE DO INPUTADO',
                'VALIDADO - PREÇO INCORRETO',
            ]
            display_note(
                df, 'Erro', st.session_state.image_index, current_errors,
                sorted(options), 'errors', set_erros
            )
    else:
        st.error("Nenhuma foto encontrada!")
else:
    st.error('Essa base de dados não é válida!')

# Exibir o rodapé
footer()
