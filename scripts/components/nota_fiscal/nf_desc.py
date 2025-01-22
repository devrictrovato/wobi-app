import pandas as pd
import streamlit as st

from scripts.utils import format_cnpj

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

# Função para exibir detalhes da Nota Fiscal
def display_nf_details(nf_info):
    """Exibir detalhes da nota fiscal em formato de tabela estilizada."""
    st.sidebar.divider()
    st.sidebar.markdown("### Informações da Nota Fiscal")
    
    nf_info['Data_da_venda'] = pd.to_datetime(nf_info['Data_da_venda'], errors='coerce')  # Converte a coluna para datetime
    nf_info['Data_da_venda'] = nf_info['Data_da_venda'].strftime('%d/%m/%Y')  # Agora aplica o formato de data

    table_html = f"""
    <table style="width:100%; font-size: 18px; border-collapse: collapse;">
        <tr><td style="font-weight: bold;">Loja:</td><td>{nf_info['Local de Atendimento Descrição']}</td></tr>
        <tr><td style="font-weight: bold;">CNPJ:</td><td>{format_cnpj(nf_info['CNPJ'])}</td></tr>
        <tr><td style="font-weight: bold;">Filial:</td><td>{nf_info['Filial']}</td></tr>
        <tr><td style="font-weight: bold;">Data da Venda:</td><td>{nf_info['Data_da_venda']}</td></tr>
        <tr><td style="font-weight: bold;">Nº da NF:</td><td>{nf_info['Numero_da_NF']}</td></tr>
        <tr><td style="font-weight: bold;">Itens Descrição:</td><td>{nf_info['Itens Descrição']}</td></tr>
        <tr><td style="font-weight: bold;">Quantidade da Venda:</td><td>{nf_info['Quantidade_venda']}</td></tr>
        <tr><td style="font-weight: bold;">Preço Unitário:</td><td>R$ {nf_info['Preco_unitario_da_venda']}</td></tr>
    </table>
    """
    
    st.sidebar.markdown(table_html, unsafe_allow_html=True)

# Função para exibir os SKUs e seus códigos
def display_nf_ids():
    st.write('### Código de SKUs')
    
    skus = [
        "43S615", "32S615", "32S5400AF", "43S5400A", "65P635", 
        "50P635", "55P635", "65P735", "50C655", "55C655", 
        "50P755", "55P755", "65P755", "75P755"
    ]
    ids_crfo = [
        '6606229', '6566057', '3194108', '3194094', '3222721', 
        '5393264', '5393248', '6942350', '3439038', '3438996', 
        '3438945', '3439020', '3439089', '3438880',
    ]

    df_skus = pd.DataFrame({'SKU': skus, 'Código do Produto': ids_crfo})
    df_skus = df_skus.sort_values(by='SKU')
    
    # Converter DataFrame para HTML com estilo customizado
    df_html = df_skus.to_html(index=False, escape=False)
    styled_html = f"<div style='font-size: 18px;'>{df_html}</div>"
    
    # Exibir DataFrame formatado
    st.markdown(styled_html, unsafe_allow_html=True)