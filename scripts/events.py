import streamlit as st

# Getters
def get_current_status(df, image_index):
    """Obtém o STATUS atual da imagem correspondente no DataFrame."""
    status = df.iloc[image_index, df.columns.get_loc("STATUS")]
    return status

def get_index_filtred_df(df, image_index):
    return df.iloc[image_index].name

# Setters
def set_status(df, image_index, new_status):
    """Atualizar o STATUS da nota fiscal."""
    temp_index = get_index_filtred_df(df, image_index)
    # st.header(temp_index)
    st.session_state.data.loc[temp_index, 'STATUS'] = new_status
    st.session_state.data.loc[temp_index, 'Quem Validou?'] = st.session_state["name"]
    st.session_state.filtred_data.loc[temp_index, 'STATUS'] = new_status
    st.session_state.filtred_data.loc[temp_index, 'Quem Validou?'] = st.session_state["name"]
    set_next_image_index(df, image_index, 1 if image_index <= df.shape[0] - 1 else 0)

def set_duplicates(df, duplicate_column):
    duplicated_mask = df.duplicated(subset=[duplicate_column], keep='first')
    first_occurrences = df[~df[duplicate_column].duplicated(keep='first') & df[duplicate_column].duplicated(keep=False)]
    st.session_state.data.loc[duplicated_mask, 'STATUS'] = 'DUPLICIDADE'
    return first_occurrences

def set_wrong_date(df, date_column):
    df.loc[df[date_column] > df['Data Hora Tarefa'], 'STATUS'] = 'DATA DIVERGENTE'

def set_no_link(df):
    df.loc[df['Foto_da_NF'] == 'http://get.umov.me/Logo/nomedia.png', 'STATUS'] = 'SEM LINK'

def set_image_index():
    # Atualiza o índice da imagem no session_state
    st.session_state.image_index = st.session_state.temp_image_index
    st.session_state.rotation_angle = 0
    if st.session_state.image_index > st.session_state.filtred_data.shape[0] - 1:
        st.session_state.image_index = st.session_state.filtred_data.shape[0] - 1
        st.session_state.finished = True
        st.success('⭐ Você chegou ao fim dessa validação!')

def set_next_image_index(df, image_index, plus):
    st.session_state.temp_image_index = image_index
    st.session_state.temp_image_index += plus
    set_image_index()
    st.session_state.status = get_current_status(df, st.session_state.image_index)

def clear_filters():
    st.session_state.image_index = 0
    st.session_state.rotation_angle = 0
    st.session_state.finished = 0
    st.session_state.filters = {}

def clear_cache():
    st.session_state.clear()