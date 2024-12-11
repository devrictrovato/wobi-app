import warnings
warnings.simplefilter(action="ignore")

import streamlit as st

def format_cnpj(cnpj):
    """Formatar CNPJ em um padrão legível."""
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def display_nf_details(nf_info):
    """Exibir detalhes da nota fiscal em formato de tabela estilizada."""
    st.sidebar.divider()
    st.sidebar.markdown("### Informações da Nota Fiscal")
    
    import pandas as pd
    nf_info['Data_da_venda'] = pd.to_datetime(nf_info['Data_da_venda'])
    nf_info['Data_da_venda'] = nf_info['Data_da_venda'].strftime('%d/%m/%Y')
    # Renderizar os dados da NF como uma tabela estilizada em HTML
    st.sidebar.markdown(
        f"""
        <table style="width:100%; font-size: 18px; border-collapse: collapse;">
            <tr>
                <td style="font-weight: bold;">Loja:</td>
                <td>{nf_info['Local de Atendimento Descrição']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold;">CNPJ:</td>
                <td>{format_cnpj(nf_info['CNPJ'].astype(str))}</td>
            </tr>
            <tr>
                <td style="font-weight: bold;">Filial:</td>
                <td>{nf_info['Filial']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold;">Data da Venda:</td>
                <td>{nf_info['Data_da_venda']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold;">Nº da NF:</td>
                <td>{nf_info['Numero_da_NF']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold;">Itens Descrição:</td>
                <td>{nf_info['Itens Descrição']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold;">Quantidade da Venda:</td>
                <td>{nf_info['Quantidade_venda']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold;">Preço Unitário:</td>
                <td>R$ {nf_info['Preco_unitario_da_venda']:.2f}</td>
            </tr>
        </table>
        """,
        unsafe_allow_html=True,
    )
