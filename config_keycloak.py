import streamlit as st
from pymongo import MongoClient
from datetime import datetime
from streamlit_keycloak import login

def main2():
    st.subheader(f" {keycloak.user_info.get('preferred_username', 'User')}!")
    # st.write(asdict(keycloak))
    if st.button("Disconnect"):
        keycloak.authenticated = False



    keycloak = login(
        url="http://localhost:8080",
        realm="humanmigration",
        client_id="humanmigration",
    )

    if keycloak.authenticated:
        # st.write(keycloak.user_info)  # Debugging line
        st.write("Authentication success.")
        main2()
    else:
        st.write("Sign In !")