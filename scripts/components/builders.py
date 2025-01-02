import streamlit as st
import streamlit_image_zoom
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

from scripts.data.data import convert_to_csv, convert_to_excel
from scripts.events import clear_filters, set_duplicates, set_image_index, set_no_link, set_status, set_wrong_date
from scripts.components.images import load_image, rotate_image

def nf_explain():
    # Subtítulo
    st.divider()
    st.subheader("Notas Fiscais")

    # Explicação básica
    with st.expander(
        'Verifique o formato das colunas da base SELLOUT para a validação de NFs.',
    ):
        # Configuração de colunas
        data_columns = [
            'Local de Atendimento Descrição',
            'CNPJ',
            'Filial',
            'Itens Descrição',
            'Preco_unitario_da_venda',
            'Quantidade_venda',
            'Data_da_venda',
            'Numero_da_NF',
            'Foto_da_NF',
            'Foto_da_NF_2',
            'Foto_da_NF_3',
            'STATUS'
        ]
        st.pills('Configuração (considere as letras maiúsculas e minúsculas e caracteres especiais)', data_columns, disabled=True)
    st.divider()

def nf_show():
    with st.expander('Opções extras'):
        col1, col2, col3, col4 = st.columns(4, vertical_alignment='center')
        with col1: nf_duplicates(st.session_state.data)
        with col2: nf_wrong_date(st.session_state.data)
        with col3: nf_no_media(st.session_state.data)
        with col4: nf_clear_cache()
    # Exibir dados filtrados
    st.subheader("Exibindo Dados Originais (Importados/Exportados)")
    st.dataframe(st.session_state.data.drop(columns=['Mes_da_venda', 'Duplicidade']))

    st.subheader("Dados Filtrados (Opicional)")
    st.dataframe(st.session_state.filtred_data.drop(columns=['Mes_da_venda', 'Duplicidade']))

def nf_links(images):
    # Campo numérico para selecionar a imagem pelo índice
    st.number_input(
        "Defina o índice da imagem:",
        value=st.session_state.image_index,  # O valor inicial vem do session_state
        min_value=0,
        max_value=len(images) - 1,
        step=1,
        key='temp_image_index',
        on_change=set_image_index,
    )

def nf_photo(current_image, image_paths):
        # Carregar a imagem atual
    foto_imagem = load_image(current_image)
    
    # foto_atual = st.image(
    #     foto_imagem,
    #     caption=f"Foto {st.session_state.image_index + 1} / {len(image_paths)}",
    #     # width=1000,
    #     use_container_width=True,
    # )
    # Exibir a imagem com zoom e manter o aspecto
    with st.container():
        # Dimensões ajustadas dinamicamente para o zoom
        zoom_width =  max(800, int(foto_imagem.width * .4))
        zoom_height = max(800, int(foto_imagem.height * .4))
        
        foto_atual = streamlit_image_zoom.image_zoom(
            foto_imagem,
            zoom_factor=3,
            keep_aspect_ratio=True,
            keep_resolution=True,
            size=(zoom_width, zoom_height),
        )

    # Desenvolver o caption para apresentar X/XX de imagens
    image_index = st.session_state.get("image_index", 0) + 1
    total_images = len(image_paths)
    caption_text = f"Foto {image_index} / {total_images}"

    # Mostrar o caption abaixo da imagem

    st.caption(f'<div style="margin-bottom: 25px; text-align: center;">{caption_text}</div>', unsafe_allow_html=True)

    # Realizar rotação da imagem se necessário
    rotate_image(foto_atual, foto_imagem)

def nf_status(df, image_index, current_status):
    status_options = sorted([
        'PENDENTE', 'APROVADO',
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
            df, image_index, st.session_state.status
        ),
        index=status_options.index(current_status) if current_status in status_options else 0,
    )

def nf_duplicates(df):
    # Botões auxiliares
    if st.button("🚀 Duplicatas", disabled=False):
        with st.spinner("Processando..."):
            set_duplicates(df, 'Duplicidade')
            st.success("Duplicidades Marcadas!")
    # st.dataframe(df[df.duplicated(subset=['Duplicidade'], keep='first')])

def nf_wrong_date(df):
    if st.button('📅 Datas', disabled=False):
        with st.spinner("Processando..."):
            set_wrong_date(df, 'Data_da_venda')
            st.success("Datas Divergentes Marcadas!")

def nf_no_media(df):
    if st.button('🔗 NoMedia', disabled=False):
        with st.spinner("Processando..."):
            set_no_link(df)
            st.success("NoMedia Marcados!")

def nf_clear_cache():
    if st.button('♻️ Limpar Cache', disabled=False):
        with st.spinner("Processando..."):
            clear_filters()
            st.success("Cache Liberado!")

def exports():
    # Botões de exportação
    st.markdown("### Exportar Dados:")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="⬇️ Exportar para Excel",
            data=convert_to_excel(st.session_state.data),
            file_name="CHECKPOINT.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col2:
        st.download_button(
            label="⬇️ Exportar para CSV",
            data=convert_to_csv(st.session_state.data),
            file_name="CHECKPOINT.csv",
            mime="text/csv"
        )

def login():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    stauth.Hasher.hash_passwords(config['credentials'])

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )

    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

    if st.session_state['authentication_status']:
        col1, col2 = st.columns(2, vertical_alignment='center')
        with col1: st.write(f'### 💻 *{st.session_state["name"]}*')
        with col2: authenticator.logout()
        return True
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

    return False

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