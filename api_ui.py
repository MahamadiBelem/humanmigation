import streamlit as st
import requests

def open_api_migrate():
    st.title("Données de Migration Humaine")

    # Afficher les données
    if st.button("Afficher les données"):
        response = requests.get("http://localhost:8510/api/insp/donnee-migration-humaine")
        data = response.json().get("data", [])
        st.write(data)

    # Ajouter des données
    st.header("Ajouter des données")
    field1 = st.text_input("Field1")
    field2 = st.number_input("Field2", min_value=0)

    if st.button("Ajouter"):
        new_data = {"field1": field1, "field2": field2}
        response = requests.post("http://localhost:8501/api/insp/donnee-migration-humaine", json=new_data)
        st.write(response.json())

