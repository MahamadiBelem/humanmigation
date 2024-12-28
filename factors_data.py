import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu
import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from bson.objectid import ObjectId
from streamlit_option_menu import option_menu


# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['factors_db']
collection = db['my_factors_db']
metadata_collection = db['metadata']




# ****************************************************************************************
# *****************************************************************************************



required_columns = ['year', 'factor', 'type', 'location', 'valeur']

# Fonctionnalité 1: Charger un fichier
def charger_fichier_factors():
    st.header("Charger un fichier")
    uploaded_file1 = st.file_uploader("Choisir un fichier CSV, Excel ou JSON", type=["csv", "xlsx", "json"])

    if uploaded_file1 is not None:
        if uploaded_file1.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file1)
        elif uploaded_file1.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file1)
        elif uploaded_file1.name.endswith('.json'):
            df = pd.read_json(uploaded_file1)
        
        # Vérifier si les colonnes requises sont présentes
        if all(column in df.columns for column in required_columns):
            st.success("Le fichier contient toutes les colonnes requises.")
            
            type_fichier = st.selectbox("Data type", ["Migration Data", "Spatiale Data", "Factors Data"])
            auteur = st.text_input("Auteur")
            description = st.text_area("Description")
            date_chargement = st.date_input("Date de chargement", datetime.now())
            date_fin = st.date_input("Date de fin")
            visibilite = st.selectbox("Visibilité", ["Public", "Privé"])
            
            if st.button("Enregistrer"):
                metadata = {
                    "type_fichier": type_fichier,
                    "auteur": auteur,
                    "description": description,
                    "date_chargement": date_chargement.strftime("%Y-%m-%d"),
                    "date_fin": date_fin.strftime("%Y-%m-%d"),
                    "visibilite": visibilite,
                    "data": df.to_dict(orient="records")
                }
                metadata_collection.insert_one(metadata)
                st.success("Fichier enregistré avec succès!")
        else:
            st.error("Le fichier ne contient pas toutes les colonnes requises.")




required_columns = ['year','factor','type','location','valeur']

# Fonctionnalité 1: Charger un fichier
def charger_fichier_factors_ok():
    st.header("Charger un fichier")
    uploaded_file1 = st.file_uploader("Choisir un fichier CSV ou Excel", type=["csv", "xlsx"])


    
    if uploaded_file1 is not None:
        if uploaded_file1.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file1)
        else:
            df = pd.read_excel(uploaded_file1)
        
        # Vérifier si les colonnes requises sont présentes
        if all(column in df.columns for column in required_columns):
            st.success("Le fichier contient toutes les colonnes requises.")
            
            type_fichier = st.selectbox("Data type",["Migration Data","Spatiale Data,", "Factors Data"])
            auteur = st.text_input("Auteur")
            description = st.text_area("Description")
            date_chargement = st.date_input("Date de chargement", datetime.now())
            date_fin = st.date_input("Date de fin")
            visibilite = st.selectbox("Visibilité", ["Public", "Privé"])
            
            if st.button("Enregistrer"):
                metadata = {
                    "type_fichier": type_fichier,
                    "auteur": auteur,
                    "description": description,
                    "date_chargement": date_chargement.strftime("%Y-%m-%d"),
                    "date_fin": date_fin.strftime("%Y-%m-%d"),
                    "visibilite": visibilite,
                    "data": df.to_dict(orient="records")
                }
                metadata_collection.insert_one(metadata)
                st.success("Fichier enregistré avec succès!")
        else:
            st.error("Le fichier ne contient pas toutes les colonnes requises.")




def consult_data():
     # Récupérer les fichiers
        fichiers = list(metadata_collection.find())
        
        # Créer une liste d'IDs personnalisés
        fichier_ids = []
        for index, fichier in enumerate(fichiers, start=1):
            auteur = fichier.get("auteur", "inconnu")
            annee = datetime.now().year
            id_personnalise = f"{auteur}_{annee}_{index:04d}"
            fichier_ids.append((id_personnalise, str(fichier["_id"])))
        
        # Afficher les IDs personnalisés dans le selectbox
        fichier_choisi = st.selectbox("Choisir un fichier à consulter", fichier_ids, format_func=lambda x: x[0])
        
        if fichier_choisi:
            fichier = metadata_collection.find_one({"_id": ObjectId(fichier_choisi[1])})
            df = pd.DataFrame(fichier["data"])
            
            with st.sidebar:
                visualization_type = option_menu(
                    'Choisir le type de visualisation:',
                    ['Tabulaire', 'Bar Chart', 'Line Chart', 'Area Chart'],
                    icons=['list', 'bar-chart', 'line-chart', 'area-chart'],
                    menu_icon="cast",
                    default_index=0,
                    orientation='vertical'
                )

            st.write(f'Vous avez sélectionné : {visualization_type}')

            if visualization_type == 'Tabulaire':
                st.write(df)

            elif visualization_type == 'Bar Chart':
                st.bar_chart(df.set_index('year')[['valeur']])

            elif visualization_type == 'Line Chart':
                st.line_chart(df.set_index('year')[['valeur']])


# charger_fichier_factors()
# consult_data()