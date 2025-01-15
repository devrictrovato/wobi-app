import yaml

import streamlit_authenticator as stauth
import streamlit as st

from scripts.events import clear_cache


def login():
    """
    Realiza o login utilizando o streamlit_authenticator.
    """
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    stauth.Hasher.hash_passwords(config['credentials'])
    authenticator = stauth.Authenticate(
        config['credentials'], config['cookie']['name'],
        config['cookie']['key'], config['cookie']['expiry_days']
    )

    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

    if st.session_state['authentication_status']:
        col1, col2 = st.columns(2, vertical_alignment='center')
        st.session_state["name"] = st.session_state["name"].split(' ')[0]
        with col1: st.write(f'### 🔑 *{st.session_state["name"]}*')
        with col2: authenticator.logout(callback=clear_cache)
        return True
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

    return False