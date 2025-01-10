import streamlit as st

from scripts.events import (
    clear_filters, set_duplicates, set_image_index, 
    set_no_link, set_wrong_date
)
from scripts.components.images import load_image, rotate_image

def nf_explain():
    """
    Exibe as explicações sobre o formato das colunas da base SELLOUT para a validação de NFs.
    """
    st.divider()
    st.subheader("Notas Fiscais")

    with st.expander('Verifique o formato das colunas da base SELLOUT para a validação de NFs.'):
        data_columns = [
            'Local de Atendimento Descrição', 'CNPJ', 'Filial', 'Itens Descrição', 
            'Preco_unitario_da_venda', 'Quantidade_venda', 'Data_da_venda', 
            'Numero_da_NF', 'Foto_da_NF', 'Foto_da_NF_2', 'Foto_da_NF_3', 'STATUS'
        ]
        st.pills('Configuração (considere as letras maiúsculas e minúsculas e caracteres especiais)', data_columns, disabled=True)
    st.divider()

def extra_options():
    """
    Exibe as opções extras de filtros para Notas Fiscais.
    """
    with st.expander('Opções extras'):
        if st.session_state.type_data == 'NF':
            col1, col2, col3, col4 = st.columns(4, vertical_alignment='center')
            with col1: nf_duplicates(st.session_state.data)
            with col2: nf_wrong_date(st.session_state.data)
            with col3: nf_no_media(st.session_state.data)
            with col4: nf_clear_cache()

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

        foto_atual = image_zoom(foto_imagem, zoom_factor=3, size=(800, 800))
        # st.caption(caption_text)
    else:
        foto_atual = st.image(foto_imagem, caption=caption_text, use_container_width=True,)

    # Girar imagem se necessário
    rotate_image(foto_atual, foto_imagem)

def display_note(df, column, image_index, current_status, options, key, change_func):
    st.sidebar.selectbox(
        f"Alterar {column}:",
        options=options,
        key=key,
        on_change=lambda: change_func(df, image_index, st.session_state[key]),
        index=options.index(current_status) if current_status in options else 0,
    )

def nf_duplicates(df):
    """
    Marca as duplicatas encontradas na base de dados.
    """
    if st.button("🚀 Duplicatas", disabled=False):
        with st.spinner("Processando..."):
            set_duplicates(df, 'Duplicidade')
            st.success("Duplicidades Marcadas!")

def nf_wrong_date(df):
    """
    Marca as datas divergentes.
    """
    if st.button('📅 Datas', disabled=False):
        with st.spinner("Processando..."):
            set_wrong_date(df, 'Data_da_venda')
            st.success("Datas Divergentes Marcadas!")

def nf_no_media(df):
    """
    Marca as notas fiscais sem link para imagem.
    """
    if st.button('🔗 NoMedia', disabled=False):
        with st.spinner("Processando..."):
            set_no_link(df)
            st.success("NoMedia Marcados!")

def nf_clear_cache():
    """
    Limpa os filtros e reseta as variáveis.
    """
    if st.button('♻️ Limpar Cache', disabled=False):
        with st.spinner("Processando..."):
            clear_filters()
            st.success("Cache Liberado!")
