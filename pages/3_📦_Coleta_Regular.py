# Bibliotecas
import streamlit as st
import pandas as pd
from streamlit_image_select import image_select

from scripts.components.builders import display_note, photo, image_index_input
from scripts.components.coleta_regular.cr_desc import display_cr_details
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
    links = ["Tire_uma_foto_comprovando_o_preco_do_produto_etiqueta_ou_tela_do_sistema", "Mosaico"]
    foto_coluna = st.sidebar.selectbox("Selecione uma Foto:", links)

    if foto_coluna == links[-1]:
        image_paths = df[links[0]].to_list()  # Filtra valores

        # Selecionar o número de amostras
        col1, col2 = st.columns(2)
        with col1:
            selected_lote = st.number_input(
                'Numero do lote',
                min_value=0,
                value=0, 
                key='lote'
            )
        with col2:
            selected_batch = st.number_input(
                'Número de amostras', 
                min_value=1, 
                max_value=len(image_paths)-1,
                value=32,
                key='batchs'
            )

        temp = image_paths[selected_batch * selected_lote: selected_batch * (selected_lote + 1)]

        # Exibir mosaico de imagens
        selected_image = None
        try:
            selected_image = image_select(
                label="Selecione uma imagem",
                images=temp,
                # captions=[f"Foto {i+1}" for i in range(len(image_paths))],
                use_container_width=True,
            )
        except:
            st.warning('Nenhuma imagem selecionada!')

        if selected_image:
            st.session_state.image_index = image_paths.index(selected_image)
            current_image = selected_image

            if pd.isna(current_image):
                st.error('Foto não encontrada! (selecione outra foto)')
            else:
                # Exibir a foto atual e informações
                # photo(current_image, image_paths)
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
                    sorted(options), 'errors', set_erros, False
                )
    else:
        image_paths = df[foto_coluna].to_list()  # Filtra valores

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
