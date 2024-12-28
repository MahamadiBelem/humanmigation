# import os
# import pandas as pd
# from pyspark.sql import SparkSession
# import streamlit as st
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import folium_static
# import streamlit as st
# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import folium
# from streamlit_folium import folium_static
# from streamlit_option_menu import option_menu

# # Configurer les variables d'environnement pour PySpark
# os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
# os.environ["PYSPARK_PYTHON"] = "python"  # Assurez-vous que "python" est accessible via PATH
# os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

# # Créer une session Spark
# spark = SparkSession.builder.appName("MigrationData").getOrCreate()

# # Fonction pour créer une carte avec les migrations internes
# def create_internal_map(data):
#     m = folium.Map(location=[12.3714, -1.5197], zoom_start=6)  # Centré sur le Burkina Faso

#     marker_cluster = MarkerCluster().add_to(m)

#     for index, row in data.iterrows():
#         folium.Marker(
#             location=[row['Latitude_From'], row['Longitude_From']],
#             popup=f"From: {row['From_City']}",
#             icon=folium.Icon(color="blue")
#         ).add_to(marker_cluster)

#         folium.Marker(
#             location=[row['Latitude_To'], row['Longitude_To']],
#             popup=f"To: {row['To_City']}",
#             icon=folium.Icon(color="red")
#         ).add_to(marker_cluster)

#         folium.PolyLine(
#             locations=[(row['Latitude_From'], row['Longitude_From']), (row['Latitude_To'], row['Longitude_To'])],
#             color="green"
#         ).add_to(m)

#     return m

# # Fonction pour créer une carte avec les migrations entre pays
# def create_international_map(data):
#     m = folium.Map(location=[9.082, 8.6753], zoom_start=5)  # Centré sur l'Afrique de l'Ouest

#     marker_cluster = MarkerCluster().add_to(m)

#     for index, row in data.iterrows():
#         folium.Marker(
#             location=[row['Latitude_From'], row['Longitude_From']],
#             popup=f"From: {row['From_Country']}",
#             icon=folium.Icon(color="blue")
#         ).add_to(marker_cluster)

#         folium.Marker(
#             location=[row['Latitude_To'], row['Longitude_To']],
#             popup=f"To: {row['To_Country']}",
#             icon=folium.Icon(color="red")
#         ).add_to(marker_cluster)

#         folium.PolyLine(
#             locations=[(row['Latitude_From'], row['Longitude_From']), (row['Latitude_To'], row['Longitude_To'])],
#             color="green"
#         ).add_to(m)

#     return m

# # Fonction pour lire le fichier téléchargé
# def load_data(file_path):
#     if file_path.endswith(".csv"):
#         df = pd.read_csv(file_path)
#     elif file_path.endswith(".xlsx"):
#         df = pd.read_excel(file_path)
#     else:
#         st.error("Format de fichier non supporté!")
#         return None
    
#     return df

# # Créer le répertoire si nécessaire
# save_directory = "C:\\fichier\\spatiale"
# os.makedirs(save_directory, exist_ok=True)




# # Initialiser Spark
# spark = SparkSession.builder.appName("MigrationData").getOrCreate()

# # Fonction pour charger les données
# def load_data(file_path):
#     if file_path.endswith('.csv'):
#         return pd.read_csv(file_path)
#     elif file_path.endswith('.xlsx'):
#         return pd.read_excel(file_path)
#     return None

# # Fonction pour créer un graphique des migrations
# def create_migration_chart(data):
#     plt.figure(figsize=(10, 6))
#     sns.barplot(x='From_Country', y='To_Country', data=data)
#     plt.title('Migrations entre les pays de l\'Afrique de l\'Ouest')
#     plt.xticks(rotation=45)
#     st.pyplot(plt)

# # Fonction pour créer un diagramme en bâtons
# def create_bar_chart(data):
#     plt.figure(figsize=(10, 6))
#     sns.barplot(x=data['To_Country'], y=data['From_Country'])
#     # sns.barplot(x=data['From_Country'], y=data['To_Country'], orient='h')
#     plt.title('Diagramme en bâtons')
#     st.pyplot(plt)

# # Fonction pour créer un diagramme circulaire
# def create_pie_chart(data):
#     plt.figure(figsize=(8, 8))
#     data['From_Country'].value_counts().plot.pie(autopct='%1.1f%%')
#     plt.title('Diagramme circulaire')
#     st.pyplot(plt)

# # Fonction pour créer un histogramme
# def create_histogram(data):
#     plt.figure(figsize=(10, 6))
#     sns.histplot(data['From_Country'], bins=30)
#     plt.title('Histogramme')
#     st.pyplot(plt)

# # Fonction pour créer un nuage de points
# def create_scatter_plot(data):
#     plt.figure(figsize=(10, 6))
#     sns.scatterplot(x=data['From_Country'], y=data['To_Country'])
#     plt.title('Nuage de points')
#     st.pyplot(plt)

# def upload_file_spatiale():
#     uploaded_file = st.file_uploader("Choisissez un fichier", type=["csv", "xlsx"])

#     if uploaded_file is not None:
#         save_directory = "C:\\fichier\\spatiale"  # Remplacez par le chemin de votre répertoire de sauvegarde
#         file_path = os.path.join(save_directory, uploaded_file.name)
        
#         # Enregistrer le fichier téléchargé
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
        
#         st.success(f"Fichier sauvegardé dans {file_path}")
        
#         data = load_data(file_path)

#         if data is not None:
#             st.write("Données spatiales:")
#             st.write(data.head())

#             # Convertir les données Pandas DataFrame en Spark DataFrame
#             spark_df = spark.createDataFrame(data)

#             # Afficher le schéma du DataFrame Spark
#             spark_df.printSchema()

# # Interface utilisateur
# # st.title("Migrations en Afrique de l'Ouest")
# # st.write("Téléchargez un fichier CSV ou Excel contenant les données de migration ou consultez les fichiers enregistrés.")

# # # Créez un menu d'options
# # file_option = option_menu(
# #     menu_title='Choisissez une option',
# #     options=['Télécharger un nouveau fichier', 'fichiers spatiales'],
# #     icons=['cloud-upload', 'map'],
# #     menu_icon='cast',
# #     default_index=0,
# # )

  
# def consulation_spatiale():
#     save_directory = "C:\\fichier\\spatiale"  # Remplacez par le chemin de votre répertoire de sauvegarde
#     files = os.listdir(save_directory)
#     selected_file = st.selectbox('Choisissez un fichier ', files)
    
#     if selected_file:
#         file_path = os.path.join(save_directory, selected_file)
        
#         data = load_data(file_path)

#         if data is not None:
#             with st.sidebar:
#                 selected = option_menu(
#                     menu_title=None,  # Titre du menu, si None, pas de titre
#                     options=["Tabulaire", "Carte", "circulaire", "Histogramme", "Nuage Points"],  # Options du menu
#                     icons=["house", "map", "bar-chart", "pie-chart", "histogram", "scatter-plot"],  # Icônes pour chaque option
#                     menu_icon="cast",  # Icône du menu
#                     default_index=0,  # Option sélectionnée par défaut
#                     orientation="vertical"  # Orientation du menu
#                 )

#             # Affichage en fonction de l'option sélectionnée
#             if selected == "Tabulaire":
#                 st.write(data.head())
#             # Convertir les données Pandas DataFrame en Spark DataFrame
#                 spark_df = spark.createDataFrame(data)
#             # Afficher le schéma du DataFrame Spark
#                 spark_df.printSchema()
#                 # Ajouter un bouton pour télécharger les données affichées
#                 def convert_df(df):
#                     return df.to_csv(index=False).encode('utf-8')

#                 csv = convert_df(data)

#                 st.download_button(
#                     label="Télécharger les données en CSV",
#                     data=csv,
#                     file_name='data.csv',
#                     mime='text/csv',
#                 )
#             elif selected == "Carte":
#                 map_ = create_international_map(data)
#                 st.write("Carte des migrations:")
#                 folium_static(map_)
#             # elif selected == "Graphique":
#             #     st.write("Graphique des migrations:")
#             #     create_migration_chart(data)
#             elif selected == "bâtons":
#                 st.write("Diagramme en bâtons des migrations:")
#                 create_bar_chart(data)
#             elif selected == "circulaire":
#                 st.write("Diagramme circulaire des migrations:")
#                 create_pie_chart(data)
#             elif selected == "Histogramme":
#                 st.write("Histogramme des migrations:")
#                 create_histogram(data)
#             elif selected == "Nuage Points":
#                 st.write("Nuage de points des migrations:")
#                 create_scatter_plot(data)

