# main_app.py
import os
import streamlit as st
from archive.migration_maps import save_uploaded_file, load_data, display_migration_map, spark
from streamlit_folium import folium_static  # Import the folium_static function

# Créer le répertoire si nécessaire
save_directory = "C:\\fichier\\spatiale"
os.makedirs(save_directory, exist_ok=True)

def main2():
    st.title("Migrations en Afrique de l'Ouest")
    st.write("Téléchargez un fichier CSV ou Excel contenant les données de migration ou consultez les fichiers enregistrés.")

    option = st.selectbox(
        'Choisissez le type de migration à visualiser',
        ('Migrations internes au Burkina Faso', 'Migrations entre pays de l\'Afrique de l\'Ouest')
    )

    file_option = st.radio(
        'Choisissez une option',
        ('Télécharger un nouveau fichier', 'Consulter les fichiers enregistrés')
    )

    if file_option == 'Télécharger un nouveau fichier':
        uploaded_file = st.file_uploader("Choisissez un fichier", type=["csv", "xlsx"])

        if uploaded_file is not None:
            file_path = save_uploaded_file(uploaded_file, save_directory)
            st.success(f"Fichier sauvegardé dans {file_path}")
            
            data = load_data(file_path)

            if data is not None:
                st.write("Aperçu des données téléchargées:")
                st.write(data.head())

                # Convertir les données Pandas DataFrame en Spark DataFrame
                spark_df = spark.createDataFrame(data)
                spark_df.printSchema()

                # Créer la carte selon le type de migration sélectionné
                map_ = display_migration_map(data, option)

                # Afficher la carte avec Folium
                st.write("Carte des migrations:")
                folium_static(map_)

    elif file_option == 'Consulter les fichiers enregistrés':
        files = os.listdir(save_directory)
        selected_file = st.selectbox('Choisissez un fichier enregistré', files)
        
        if selected_file:
            file_path = os.path.join(save_directory, selected_file)
            data = load_data(file_path)

            if data is not None:
                st.write("Aperçu des données téléchargées:")
                st.write(data.head())

                # Convertir les données Pandas DataFrame en Spark DataFrame
                spark_df = spark.createDataFrame(data)
                spark_df.printSchema()

                # Créer la carte selon le type de migration sélectionné
                map_ = display_migration_map(data, option)

                # Afficher la carte avec Folium
                st.write("Carte des migrations:")
                folium_static(map_)

# if __name__ == "__main__":
#     main2()
