import streamlit as st

import passwordless_api
from passwordless_auth import passwordless_auth_component

st.set_page_config(page_title="Login")
st.title("Register")

st.text_input("Username", key="username")
st.text_input("Alias", key="alias")

if st.button("Register"):
    if "auth_error" in st.session_state:
        del st.session_state.auth_error

    registered_token = passwordless_api.register(st.session_state.username, st.session_state.alias)

    st.session_state.register_token = registered_token.token

if "register_token" in st.session_state:
    auth_result = passwordless_auth_component("passwordless_auth_register", data={
        "api_url": st.secrets["passwordless_api_url"],
        "api_key": st.secrets["passwordless_api_key"],
        "type": "register",
        "token": st.session_state.register_token
    })
    print(auth_result)

    if auth_result is not None:

        if "token" in auth_result:
            st.session_state.register_auth_result = auth_result
        else:
            st.session_state.auth_error = auth_result

        del st.session_state.register_token

if "register_auth_result" in st.session_state:
    st.write("## Result: ", st.session_state.register_auth_result)

if "auth_error" in st.session_state:
    st.write("## Error: ", st.session_state.auth_error)
