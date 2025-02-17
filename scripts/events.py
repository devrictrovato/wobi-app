import streamlit as st

# Funções auxiliares para obter valores
def get_current_status(df, image_index):
    """Obtém o STATUS atual da imagem correspondente no DataFrame."""
    return df.iloc[image_index, df.columns.get_loc("STATUS")]

def get_current_errors(df, image_index):
    """Obtém o ERRO atual da imagem correspondente no DataFrame."""
    return df.iloc[image_index, df.columns.get_loc("ERRO")]

def get_index_filtred_df(df, image_index):
    """Obtém o índice da linha correspondente no DataFrame filtrado."""
    return df.iloc[image_index].name

# Funções auxiliares para atualizar valores
def update_column(df, image_index, column, new_value):
    """Atualiza uma coluna especificada no DataFrame."""
    temp_index = get_index_filtred_df(df, image_index)
    st.session_state.data.loc[temp_index, column] = new_value
    st.session_state.filtred_data.loc[temp_index, column] = new_value

def set_status(df, image_index, new_status, next_image=True):
    """Atualiza o STATUS da nota fiscal."""
    update_column(df, image_index, 'STATUS', new_status)
    update_column(df, image_index, 'Quem Validou?', st.session_state["name"])
    if next_image:
        set_next_image_index(df, image_index, 1 if image_index <= df.shape[0] - 1 else 0, 'STATUS')

def set_erros(df, image_index, new_error, next_image=True):
    """Atualiza o ERRO da nota fiscal."""
    update_column(df, image_index, 'ERRO', new_error)
    # update_column(df, image_index, 'CORREÇÃO', st.session_state["correct_price"])
    update_column(df, image_index, 'Quem Validou?', st.session_state["name"])
    if next_image:
        set_next_image_index(df, image_index, 1 if image_index <= df.shape[0] - 1 else 0, 'ERRO')

# Funções para condições específicas
def set_duplicates(duplicate_column):
    # Cria uma máscara para identificar duplicatas
    duplicated_mask = st.session_state.data.duplicated(subset=[duplicate_column], keep='first')

    # Marca todas as ocorrências de duplicatas no DataFrame original
    st.session_state.data.loc[duplicated_mask, 'STATUS'] = 'DUPLICIDADE'
    st.session_state.data.loc[duplicated_mask, 'STATUS'] = 'DUPLICIDADE'

    # Retorna a última ocorrência de duplicatas
    last_occurrences_mask = st.session_state.data.duplicated(subset=[duplicate_column], keep='last')
    return st.session_state.data.loc[last_occurrences_mask]

def set_wrong_date(date_column):
    """Marca registros com data divergente."""
    st.session_state.data.loc[st.session_state.data[date_column] > st.session_state.data['Data Hora Tarefa'], 'STATUS'] = 'DATA DIVERGENTE'

def set_no_link():
    """Marca registros sem link de foto."""
    if st.session_state.type_data == 'NF':
        st.session_state.data.loc[st.session_state.data['Foto_da_NF'] == 'http://get.umov.me/Logo/nomedia.png', 'STATUS'] = 'SEM LINK'
    elif st.session_state.type_data == 'CR':
        st.session_state.data.loc[st.session_state.data['Tire_uma_foto_comprovando_o_preco_do_produto_etiqueta_ou_tela_do_sistema'] == 'http://get.umov.me/Logo/nomedia.png', 'ERRO'] = 'SEM LINK'

def set_qtd_alert(qtd_column):
    """Marca registros com quantidade divergente."""
    st.session_state.data.loc[st.session_state.data[qtd_column] <= 0, 'ERRO'] = 'ALERTA - NÚMERO DE EXPOSIÇÃO ZERADO'
    st.session_state.data.loc[st.session_state.data[qtd_column] > 3, 'ERRO'] = 'ALERTA - PRODUTOS EXPOSTOS EM EXCESSO'

# Função para atualizar o índice da imagem
def set_image_index():
    """Atualiza o índice da imagem no session_state."""
    st.session_state.image_index = st.session_state.temp_image_index
    st.session_state.rotation_angle = 0
    if st.session_state.image_index > st.session_state.filtred_data.shape[0] - 1:
        st.session_state.image_index = st.session_state.filtred_data.shape[0] - 1
        st.session_state.finished = True
        st.success('⭐ Você chegou ao fim dessa validação!')

# Função para definir o próximo índice da imagem
def set_next_image_index(df, image_index, plus, column):
    """Define o próximo índice da imagem com base na ação."""
    st.session_state.temp_image_index = image_index + plus
    set_image_index()
    if column == 'STATUS':
        st.session_state.status = get_current_status(df, st.session_state.image_index)
    elif column == 'ERRO':
        st.session_state.errors = get_current_errors(df, st.session_state.image_index)

# Funções para limpar filtros e cache
def clear_filters():
    """Limpa os filtros e restabelece os valores iniciais do session_state."""
    st.session_state.image_index = 0
    st.session_state.rotation_angle = 0
    st.session_state.finished = 0
    st.session_state.filters.clear()
    st.session_state.filtred_data = dict()

def clear_cache(logout=True):
    """Limpa o cache do session_state."""
    st.session_state.clear()
