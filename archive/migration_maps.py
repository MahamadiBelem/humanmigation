# migration_maps.py
import os
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from pyspark.sql import SparkSession

# Configurer les variables d'environnement pour PySpark
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

# Créer une session Spark
spark = SparkSession.builder.appName("MigrationData").getOrCreate()

# Fonction pour créer une carte avec les migrations internes
def create_internal_map(data):
    m = folium.Map(location=[12.3714, -1.5197], zoom_start=6)  # Centré sur le Burkina Faso
    marker_cluster = MarkerCluster().add_to(m)
    
    for index, row in data.iterrows():
        folium.Marker(
            location=[row['Latitude_From'], row['Longitude_From']],
            popup=f"From: {row['From_City']}",
            icon=folium.Icon(color="blue")
        ).add_to(marker_cluster)
        
        folium.Marker(
            location=[row['Latitude_To'], row['Longitude_To']],
            popup=f"To: {row['To_City']}",
            icon=folium.Icon(color="red")
        ).add_to(marker_cluster)
        
        folium.PolyLine(
            locations=[(row['Latitude_From'], row['Longitude_From']), (row['Latitude_To'], row['Longitude_To'])],
            color="green"
        ).add_to(m)
    
    return m

# Fonction pour créer une carte avec les migrations entre pays
def create_international_map(data):
    m = folium.Map(location=[9.082, 8.6753], zoom_start=5)  # Centré sur l'Afrique de l'Ouest
    marker_cluster = MarkerCluster().add_to(m)
    
    for index, row in data.iterrows():
        folium.Marker(
            location=[row['Latitude_From'], row['Longitude_From']],
            popup=f"From: {row['From_Country']}",
            icon=folium.Icon(color="blue")
        ).add_to(marker_cluster)
        
        folium.Marker(
            location=[row['Latitude_To'], row['Longitude_To']],
            popup=f"To: {row['To_Country']}",
            icon=folium.Icon(color="red")
        ).add_to(marker_cluster)
        
        folium.PolyLine(
            locations=[(row['Latitude_From'], row['Longitude_From']), (row['Latitude_To'], row['Longitude_To'])],
            color="green"
        ).add_to(m)
    
    return m

# Fonction pour lire le fichier téléchargé
def load_data(file_path):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        return None
    return df

# Fonction pour afficher une carte de migration
def display_migration_map(data, migration_type):
    if migration_type == 'Migrations internes au Burkina Faso':
        map_ = create_internal_map(data)
    else:
        map_ = create_international_map(data)
    
    return map_

# Fonction pour sauvegarder le fichier téléchargé
def save_uploaded_file(uploaded_file, save_directory):
    file_path = os.path.join(save_directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
