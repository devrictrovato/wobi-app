import streamlit as st

from scripts.data import convert_to_csv, convert_to_excel
from scripts.events import set_duplicates, set_image_index, set_status
from scripts.images import load_image, rotate_image

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

def nf_show(df):
    # Exibir dados filtrados
    if st.session_state.filtered_data is not None:
        st.subheader("Dados Filtrados")
        st.dataframe(st.session_state.filtered_data)
    else:
        st.subheader("Exibindo Dados")
        st.dataframe(st.session_state.filtered_data)
    with st.expander('Opções auxiliares'):
        nf_duplicates(df)

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
    foto_atual = st.image(
        foto_imagem,
        caption=f"Foto {st.session_state.image_index + 1} / {len(image_paths)}",
        # width=1000,
        use_container_width=True,
    )
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
    if st.button("🚀 Marcar Duplicatas"):
        with st.spinner("Processando..."):
            df = set_duplicates(df)
            st.success("Duplicidades Marcadas!")
    # st.dataframe(df[df.duplicated(subset=['Duplicidade'], keep='first')])

def exports(df):
    # Botões de exportação
    st.markdown("### Exportar Dados:")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="⬇️ Exportar para Excel",
            data=convert_to_excel(df),
            file_name="CHECKPOINT.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col2:
        st.download_button(
            label="⬇️ Exportar para CSV",
            data=convert_to_csv(df),
            file_name="CHECKPOINT.csv",
            mime="text/csv"
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