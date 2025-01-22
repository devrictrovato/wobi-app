import pandas as pd
import streamlit as st


def display_cr_details(cr_info):
    """Exibir detalhes da coleta regular em formato de tabela estilizada."""
    st.sidebar.divider()
    st.sidebar.markdown("### Informações da Coleta Regular")
    
    cr_info['Data Hora Tarefa'] = pd.to_datetime(cr_info['Data Hora Tarefa'], errors='coerce')  # Converte a coluna para datetime
    cr_info['Data Hora Tarefa'] = cr_info['Data Hora Tarefa'].strftime('%d/%m/%Y')  # Agora aplica o formato de data

    table_html = f"""
    <table style="width:100%; font-size: 18px; border-collapse: collapse;">
        <tr><td style="font-weight: bold;">ID Tarefa:</td><td>{cr_info['Tarefa ID para Integração']}</td></tr>
        <tr><td style="font-weight: bold;">Promotor:</td><td>{cr_info['Pessoa Nome']}</td></tr>
        <tr><td style="font-weight: bold;">Data:</td><td>{cr_info['Data Hora Tarefa']}</td></tr>
        <tr><td style="font-weight: bold;">Preço moda:</td><td>{cr_info['PREÇO MODA']}</td></tr>
        <tr><td style="font-weight: bold;">Quantidade Exposta:</td><td>{cr_info['Quantas_pecas_do_produto_estao_expostas']}</td></tr>
        <tr><td style="font-weight: bold;">SKU:</td><td>{cr_info['Itens Descrição']}</td></tr>
        <tr><td style="font-weight: bold;">Preço:</td><td>R$ {cr_info['Qual_o_preco_deste_produto']}</td></tr>
    </table>
    """
    
    st.sidebar.markdown(table_html, unsafe_allow_html=True)