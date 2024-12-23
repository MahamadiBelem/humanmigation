import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

# Connexion à MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client['test1_db']
# collection = db['test1_collection']
# metadata_collection = db['metadata']



# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['test1_db']
metadata_collection = db['metadata']

# Colonnes requises
required_columns = ['Year', 'Location', 'Origin', 'Region', 'Investment', 'Type', 'Destination', 'Age Group', 'Education Level', 'Rating', 'Migrants', 'raisons']

# Fonctionnalité 1: Charger un fichier
def charger_fichier():
    st.header("Charger un fichier")
    uploaded_file = st.file_uploader("Choisir un fichier CSV ou Excel", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Vérifier si les colonnes requises sont présentes
        if all(column in df.columns for column in required_columns):
            st.success("Le fichier contient toutes les colonnes requises.")
            
            type_fichier = st.text_input("Type de fichier")
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

# Fonctionnalité 2: Mettre à jour un fichier
def mettre_a_jour_fichier():
    st.header("Mettre à jour un fichier")
    fichiers = metadata_collection.find()
    fichier_ids = [str(fichier["_id"]) for fichier in fichiers]
    fichier_choisi = st.selectbox("Choisir un fichier à mettre à jour", fichier_ids)
    
    if fichier_choisi:
        fichier = metadata_collection.find_one({"_id": ObjectId(fichier_choisi)})
        type_fichier = st.text_input("Type de fichier", fichier["type_fichier"])
        auteur = st.text_input("Auteur", fichier["auteur"])
        description = st.text_area("Description", fichier["description"])
        date_chargement = st.date_input("Date de chargement", datetime.strptime(fichier["date_chargement"], "%Y-%m-%d"))
        date_fin = st.date_input("Date de fin", datetime.strptime(fichier["date_fin"], "%Y-%m-%d"))
        visibilite = st.selectbox("Visibilité", ["Public", "Privé"], index=["Public", "Privé"].index(fichier["visibilite"]))
        
        uploaded_file = st.file_uploader("Choisir un fichier CSV ou Excel pour mise à jour", type=["csv", "xlsx"])
        
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Vérifier si les colonnes requises sont présentes
            if all(column in df.columns for column in required_columns):
                st.success("Le fichier contient toutes les colonnes requises.")
                
                if st.button("Mettre à jour"):
                    metadata_collection.update_one(
                        {"_id": ObjectId(fichier_choisi)},
                        {"$set": {
                            "type_fichier": type_fichier,
                            "auteur": auteur,
                            "description": description,
                            "date_chargement": date_chargement.strftime("%Y-%m-%d"),
                            "date_fin": date_fin.strftime("%Y-%m-%d"),
                            "visibilite": visibilite,
                            "data": df.to_dict(orient="records")
                        }}
                    )
                    st.success("Fichier mis à jour avec succès!")
            else:
                st.error("Le fichier ne contient pas toutes les colonnes requises.")

# Fonctionnalité 3: Supprimer un fichier
def supprimer_fichier():
    st.header("Supprimer un fichier")
    fichiers = metadata_collection.find()
    fichier_ids = [str(fichier["_id"]) for fichier in fichiers]
    fichier_choisi = st.selectbox("Choisir un fichier à supprimer", fichier_ids)
    
    if fichier_choisi and st.button("Supprimer"):
        metadata_collection.delete_one({"_id": ObjectId(fichier_choisi)})
        st.success("Fichier supprimé avec succès!")

# Menu de navigation
menu = ["Charger un fichier", "Mettre à jour un fichier", "Supprimer un fichier"]
choix = st.sidebar.selectbox("Menu", menu)

if choix == "Charger un fichier":
    charger_fichier()
elif choix == "Mettre à jour un fichier":
    mettre_a_jour_fichier()
elif choix == "Supprimer un fichier":
    supprimer_fichier()
