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
    st.session_state.rotation_angle = 0
    st.session_state.data.loc[temp_index, 'STATUS'] = new_status
    st.session_state.filtered_data.loc[temp_index, 'STATUS'] = new_status
    set_next_image_index(df, image_index, 1 if image_index <= df.shape[0] - 1 else 0)

def set_duplicates(df):
    # Identificar duplicatas (excluindo a primeira ocorrência)
    df.loc[df.duplicated(subset=['Duplicidade'], keep='first'), 'STATUS'] = 'DUPLICIDADE'
    return df

def set_image_index():
    # Atualiza o índice da imagem no session_state
    st.session_state.image_index = st.session_state.temp_image_index

def set_next_image_index(df, image_index, plus):
    st.session_state.temp_image_index = image_index
    st.session_state.temp_image_index += plus
    set_image_index()
    st.session_state.status = get_current_status(df, st.session_state.image_index)