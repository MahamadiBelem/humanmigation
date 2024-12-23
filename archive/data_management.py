# data_management.py
import streamlit as st
import geopandas as gpd
import json
import pandas as pd
from pymongo import MongoClient
import os
import tempfile
import zipfile

client = MongoClient('mongodb://localhost:27017/')
db = client['data_apps']
files_collection = db['files']

def extract_zip(file):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(temp_dir)
    return temp_dir

def load_shapefile_from_zip(temp_dir):
    shp_files = [f for f in os.listdir(temp_dir) if f.endswith('.shp')]
    if not shp_files:
        st.error("Aucun fichier .shp trouvé dans le zip.")
        return None

    shp_file = shp_files[0]
    required_files = {
        'shp': os.path.join(temp_dir, shp_file),
        'shx': os.path.join(temp_dir, shp_file.replace('.shp', '.shx')),
        'dbf': os.path.join(temp_dir, shp_file.replace('.shp', '.dbf')),
    }

    if not all(os.path.exists(path) for path in required_files.values()):
        st.error("Tous les fichiers nécessaires (.shp, .shx, .dbf) doivent être présents dans le zip.")
        return None
    
    return required_files

def process_shapefile(files):
    shp_path = files['shp']
    gdf = gpd.read_file(shp_path)
    if gdf.geometry.name == 'geometry':
        gdf['latitude'] = gdf.geometry.centroid.y
        gdf['longitude'] = gdf.geometry.centroid.x
    return gdf

def process_json(file):
    data = json.load(file)
    return pd.DataFrame(data)

def save_to_mongo(file_info, gdf=None):
    if gdf is not None:
        geojson = gdf.to_json()
        file_info['data'] = geojson
    files_collection.insert_one(file_info)

def display_map(gdf):
    if 'latitude' in gdf.columns and 'longitude' in gdf.columns:
        st.write("Carte des régions :")
        st.map(gdf[['latitude', 'longitude']])
    else:
        st.error("Les colonnes 'latitude' et 'longitude' sont nécessaires pour afficher la carte.")

def show_files():
    files = files_collection.find({})
    for file in files:
        st.write(file)

def load_default_shapefile():
    shapefile_path = "path/to/burkina_faso_regions.shp"
    if os.path.exists(shapefile_path):
        gdf = gpd.read_file(shapefile_path)
        return gdf
    return None

def get_file_info():
    return {
        "author": st.text_input("Nom de l'auteur"),
        "source": st.text_input("Source du fichier"),
        "visibility": st.text_input("Visibilité"),
        "start_date": str(st.date_input("Date de début")),
        "end_date": str(st.date_input("Date de fin")),
        "description": st.text_area("Description du fichier"),
        "file_type": st.text_input("Type de fichier"),
    }

def admin_view():
    st.write("Bienvenue, administrateur !")
    st.write("Téléchargez et gérez les fichiers ici.")
    
    uploaded_file = st.file_uploader("Choisissez un fichier zip contenant les fichiers shapefile (.shp, .shx, .dbf)", type=["zip"])
    if uploaded_file:
        temp_dir = extract_zip(uploaded_file)
        files = load_shapefile_from_zip(temp_dir)
        if files:
            gdf = process_shapefile(files)
            display_map(gdf)
            
            file_info = get_file_info()
            if st.button("Sauvegarder dans MongoDB"):
                save_to_mongo(file_info, gdf)
                st.success("Fichier enregistré avec succès!")

def user_view():
    st.write("Bienvenue, utilisateur !")
    st.write("Vous pouvez consulter et télécharger les fichiers publics ici.")
    show_files()

def main():
    st.title("Application de Gestion de Données")
    
    default_gdf = load_default_shapefile()
    if default_gdf is not None:
        file_info = {
            "author": "System",
            "source": "Default",
            "visibility": "Public",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "description": "Shapefile des régions du Burkina Faso",
            "file_type": "Shapefile"
        }
        save_to_mongo(file_info, default_gdf)
        st.success("Shapefile par défaut enregistré dans MongoDB!")
    
    user_profile = st.selectbox("Sélectionnez votre profil", ["Admin", "User"])
    if user_profile == "User":
        user_view()
    elif user_profile == "Admin":
        admin_view()
