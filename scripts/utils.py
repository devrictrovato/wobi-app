from io import BytesIO
import pandas as pd
import streamlit as st

# Função para formatar CNPJ
def format_cnpj(cnpj):
    """Formatar CNPJ em um padrão legível."""
    cnpj = str(cnpj)
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def exports():
    """
    Exibe as opções de exportação de dados.
    """
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

@st.cache_data(show_spinner=False)
def convert_to_excel(df):
    """
    Converte um DataFrame para um arquivo Excel em memória.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl", mode="xlsx") as writer:
        df.to_excel(writer, index=False, sheet_name="Validação NF")
    return output.getvalue()

@st.cache_data(show_spinner=False)
def convert_to_csv(df):
    """
    Converte um DataFrame para um arquivo CSV em memória.
    """
    return df.to_csv(index=False, sep=";", encoding="utf-8").encode("utf-8")

def footer():
    """
    Exibe o rodapé da página.
    """
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