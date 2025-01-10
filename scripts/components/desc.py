import warnings
from pandas import DataFrame
import streamlit as st
import pandas as pd

# Ignorar warnings
warnings.simplefilter(action="ignore")

# Função para formatar CNPJ
def format_cnpj(cnpj):
    """Formatar CNPJ em um padrão legível."""
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

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

# Função para exibir detalhes da Coleta Regular
def display_cr_details(cr_info):
    """Exibir detalhes da coleta regular em formato de tabela estilizada."""
    st.sidebar.divider()
    st.sidebar.markdown("### Informações da Coleta Regular")
    
    cr_info['data'] = pd.to_datetime(cr_info['data'], errors='coerce')  # Converte a coluna para datetime
    cr_info['data'] = cr_info['data'].strftime('%d/%m/%Y')  # Agora aplica o formato de data
    
    table_html = f"""
    <table style="width:100%; font-size: 18px; border-collapse: collapse;">
        <tr><td style="font-weight: bold;">ID Tarefa:</td><td>{cr_info['tsk_id']}</td></tr>
        <tr><td style="font-weight: bold;">Promotor:</td><td>{cr_info['nome_promotor']}</td></tr>
        <tr><td style="font-weight: bold;">Supervisor:</td><td>{cr_info['e_supervisor']}</td></tr>
        <tr><td style="font-weight: bold;">Bandeira:</td><td>{cr_info['bandeira']}</td></tr>
        <tr><td style="font-weight: bold;">Data:</td><td>{cr_info['data']}</td></tr>
        <tr><td style="font-weight: bold;">SKU:</td><td>{cr_info['sku']}</td></tr>
        <tr><td style="font-weight: bold;">Marca:</td><td>{cr_info['marca']}</td></tr>
        <tr><td style="font-weight: bold;">Tecnologia:</td><td>{cr_info['tecnologia']}</td></tr>
        <tr><td style="font-weight: bold;">Preço:</td><td>R$ {cr_info['preço']}</td></tr>
    </table>
    """
    
    st.sidebar.markdown(table_html, unsafe_allow_html=True)

# Função para exibir os SKUs e seus códigos
def display_nf_ids():
    st.write('### Código de SKUs')
    
    skus = [
        "43S615", "32S615", "32S5400AF", "43S5400A", "65P635", 
        "50P635", "55P635", "65P735", "50C655", "55C655", 
        "50P755", "55P755", "65P755"
    ]
    ids_crfo = [
        '6606229', '6566057', '3194108', '3194094', '3222721', 
        '5393264', '5393248', '6942350', '3439038', '3438996', 
        '3438945', '3439020', '3439089',
    ]

    df_skus = DataFrame({'SKU': skus, 'Código do Produto': ids_crfo})
    df_skus = df_skus.sort_values(by='SKU')
    
    # Converter DataFrame para HTML com estilo customizado
    df_html = df_skus.to_html(index=False, escape=False)
    styled_html = f"<div style='font-size: 18px;'>{df_html}</div>"
    
    # Exibir DataFrame formatado
    st.markdown(styled_html, unsafe_allow_html=True)
