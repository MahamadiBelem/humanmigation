import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from bson.objectid import ObjectId
from streamlit_option_menu import option_menu
from PIL import Image
from home_admin_01 import home_admin
# from factors_data import consult_data
# from spatiale import consulation_spatiale
from api_ui import open_api_migrate
from prediction import main
from request_data import home_request
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_keycloak import login




# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['test_finale_db']
metadata_collection = db['metadata']



# ****************************************************************************************
# *****************************************************************************************
# # This is the global part to be appear in all page. It's follow with marque css design
# # Configuration de la page


st.set_page_config(page_title="Migration Data Hub",page_icon="🌍", layout="wide")

st.markdown("""
    <style>
        div.block-container {
            padding: 1%; /* Remove default padding */
            margin: 1%; /* Remove default margin */
            max-width: 100%; /* Ensure container takes full width */
            width: 100%; /* Ensure container takes full width */
        }
        
        .header {
            padding: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            width: 100%; /* Ensure header takes full width */
            box-sizing: border-box; /* Include padding in width calculation */
        }
        
        .marquee {
            background-color: #f0f8ff;
            color: #0b0b73;
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            white-space: nowrap;
            overflow: hidden;
            box-sizing: border-box; /* Include padding in width calculation */
            width: 100%; /* Ensure marquee takes full width */
        }
        
        .marquee span {
            display: inline-block;
            padding-left: 100%;
            animation: marquee 10s linear infinite;
        }
        
        @keyframes marquee {
            from {
                transform: translateX(0);
            }
            to {
                transform: translateX(-100%);
            }
        }
    </style>
    <div class="header">
        
    </div>
    <div class="marquee">
        <span>Welcome to the Big Data Management System!</span>
    </div>
""", unsafe_allow_html=True)




# Define required columns for different data types
required_columns_mapping = {
    "Migration Data": ['Year', 'Location', 'Origin', 'Region', 'Investment', 'Type', 'Destination', 'Age Group', 'Education Level', 'Rating', 'Migrants', 'raisons'],
    "Factors Data": ['year', 'factor', 'type', 'location', 'valeur'],
    "Spatiale Data": ['Year', 'From_Country', 'To_Country', 'Migrants', 'Latitude_From', 'Longitude_From','Latitude_To', 'Longitude_To']
}

# Function to load file to MongoDB
def charger_fichier():
    st.header("Upload a File")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
    type_fichier = st.selectbox("Data Type", list(required_columns_mapping.keys()))

    auteur = st.text_input("Author")
    description = st.text_area("Description")
    date_chargement = st.date_input("Loading Date", datetime.now())
    date_fin = st.date_input("End Date")
    visibilite = st.selectbox("Visibility", ["Public", "Private"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Get required columns for the selected type
        required_columns = required_columns_mapping[type_fichier]

        # Check if required columns are present
        if all(column in df.columns for column in required_columns):
            st.success("The file contains all required columns.")
                              
            if st.button("Save"):
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
                st.success("File uploaded successfully!")
        else:
            st.error("The file does not contain all required columns.")



def mettre_a_jour_fichier():
    st.header("Mettre à jour un fichier")
    
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
    fichier_choisi = st.selectbox("Choisir un fichier à mettre à jour", fichier_ids, format_func=lambda x: x[0])
    
    if fichier_choisi:
        fichier = metadata_collection.find_one({"_id": ObjectId(fichier_choisi[1])})
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
            required_columns = ["Year", "Migrants"]  # Exemple de colonnes requises
            if all(column in df.columns for column in required_columns):
                st.success("Le fichier contient toutes les colonnes requises.")
                
                if st.button("Mettre à jour"):
                    metadata_collection.update_one(
                        {"_id": ObjectId(fichier_choisi[1])},
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


def supprimer_fichier():
    st.header("Supprimer un fichier")
    
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
    fichier_choisi = st.selectbox("Choisir un fichier à supprimer", fichier_ids, format_func=lambda x: x[0])
    
    if fichier_choisi and st.button("Supprimer"):
        metadata_collection.delete_one({"_id": ObjectId(fichier_choisi[1])})
        st.success("Fichier supprimé avec succès!")


# Function to list all files in MongoDB with a delete link
def list_files_to_delete():
    fichiers = list(metadata_collection.find())
    fichiers_df = pd.DataFrame(fichiers, columns=["_id", "type_fichier", "auteur", "date_chargement", "description", "visibilite"])

    # Convert the MongoDB ObjectId to string for display
    fichiers_df["_id"] = fichiers_df["_id"].apply(str)

    # Add "Delete" links in the table for each file
    fichiers_df['Delete'] = fichiers_df["_id"].apply(
        lambda file_id: f'<a href="?delete_id={file_id}" class="delete-link" target="_self">🗑️Delete</a>'
    )

    # Display the table with HTML-rendered links and improved CSS
    st.write(
        fichiers_df[['type_fichier', 'auteur', 'date_chargement', 'description', 'visibilite', 'Delete']]
        .to_html(escape=False, classes="styled-table"), 
        unsafe_allow_html=True
    )

    # CSS for styling the table and delete links
    st.markdown(
        """
        <style>
        .styled-table {
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 18px;
            min-width: 400px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        }
        .styled-table th, .styled-table td {
            padding: 12px 15px;
        }
        .styled-table th {
            background-color: #009879;
            color: #ffffff;
            text-align: center;
        }
        .styled-table td {
            text-align: center;
            border-bottom: 1px solid #dddddd;
        }
        .styled-table tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }
        .styled-table tr:hover {
            background-color: #f1f1f1;
        }
        .delete-link {
            color: red;
            text-decoration: none;
            font-weight: bold;
        }
        .delete-link:hover {
            color: darkred;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )





def consulter_donnees_tab():
    st.header("Consulter les données")
    
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
        st.write(df)





def consulter_metadata():
    st.header("Consulter les métadonnées des fichiers")

    # Retrieve all files from the collection
    fichiers = metadata_collection.find()

    # Create a list of file descriptions or IDs for the selectbox
    fichier_ids = [f"{fichier['auteur']} - {fichier['date_chargement']}" for fichier in fichiers]
    
    # Select a file to view its metadata
    fichier_choisi = st.selectbox("Choisir un fichier pour voir les métadonnées", fichier_ids)
    
    if fichier_choisi:
        # Find the selected file's metadata
        fichier = metadata_collection.find_one({"auteur": fichier_choisi.split(' - ')[0], "date_chargement": fichier_choisi.split(' - ')[1]})
        
        if fichier:
            # Display metadata
            st.subheader("Métadonnées du fichier")
            st.text(f"Type de fichier: {fichier['type_fichier']}")
            st.text(f"Auteur: {fichier['auteur']}")
            st.text(f"Description: {fichier['description']}")
            st.text(f"Date de chargement: {fichier['date_chargement']}")
            st.text(f"Date de fin: {fichier['date_fin']}")
            st.text(f"Visibilité: {fichier['visibilite']}")
            
            # Optionally show the data stored in the file
            if st.checkbox("Afficher les données du fichier"):
                df = pd.DataFrame(fichier['data'])
                st.dataframe(df)
        else:
            st.error("Fichier non trouvé.")



def consulter_donnees():
    # st.header("Consulter les données")


    with st.sidebar:
                file_option = option_menu(
                    menu_title=None,  # Titre du menu, si None, pas de titre
                    options=["Spatiale Data", "Migration Data", "Factors Data"],  # Options du menu
                    icons=["house", "map", "bar-chart", "pie-chart", "histogram"],  # Icônes pour chaque option
                    menu_icon="cast",  # Icône du menu
                    default_index=0,  # Option sélectionnée par défaut
                    orientation="vertical"  # Orientation du menu
                )

    
    if file_option == 'Spatiale Data':
        st.header("Page spatiale Data")
        # consulation_spatiale()
    elif file_option == 'Factors Data':
        st.header("Page Factors Data")
        # consult_data()
    elif file_option == "Migration Data":


        fichiers = list(metadata_collection.find())

        # Convertir la liste en DataFrame
        df = pd.DataFrame(fichiers)

        # Supprimer les colonnes 'description', 'visibilite', 'data', '_id'
        df = df.drop(columns=['description', 'visibilite', 'data', '_id'])

        # Créer les fichier_ids
        fichier_ids = [(f"{fichier.get('auteur', 'inconnu')}_{datetime.now().year}_{index:04d}", str(fichier["_id"])) 
                    for index, fichier in enumerate(fichiers, start=1)]

        # Afficher les boutons radio pour chaque fichier
        fichier_choisi = st.radio("Choisir un fichier à consulter", fichier_ids, format_func=lambda x: x[0])

        st.dataframe(fichier_choisi)

        # Ajouter la colonne 'view' avec fichier_ids
        df['view'] = [f"Details for {fichier[0]}" for fichier in fichier_ids]

        # Afficher le DataFrame sans ces colonnes
        st.dataframe(df)


        # Process the selected file
        if fichier_choisi:
            fichier = metadata_collection.find_one({"_id": ObjectId(fichier_choisi[1])})
            if fichier and "data" in fichier:
                df = pd.DataFrame(fichier["data"])
                st.write(f"Données pour le fichier {fichier_choisi[0]}:")
                # st.dataframe(df)

            
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
                st.bar_chart(df.set_index('Year')[['Migrants']])

            elif visualization_type == 'Line Chart':
                st.line_chart(df.set_index('Year')[['Migrants']])

            elif visualization_type == 'Area Chart':
                st.area_chart(df.set_index('Year')[['Migrants']])



# Function to display the welcome page
def display_welcome_page():
    # Load the background image
    image = Image.open("assets/img/img5.jpg")

    # Title and slogan
    st.markdown("<h1 style='text-align: center; color: #004d99;'>Migration Data Hub</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #0066cc;'>Your portal to explore, analyze, and visualize migration data.</h2>", unsafe_allow_html=True)
    
    st.header("Overview")
    st.write("""
        <div style="text-align: center;">
            Dealing with population migration is a significant challenge for policymakers, especially in developing countries. The lack of relevant data and tools hinders effective migration policy formulation and implementation.
        </div>
    """, unsafe_allow_html=True)

    # Show the background image
    st.image(image, use_column_width=True)

    st.write("""
        <h2 style="text-align: center; color: #e74c3c;">
            Challenges
        </h2>
    """, unsafe_allow_html=True)
    st.write("""
        <div style="text-align: center;">
            <ul style="list-style-type: none;">
                <li><span style="color: #e74c3c;">1. <strong>Data Fragmentation</strong></span>: Researchers collect data in various formats for different purposes, leading to fragmented information.</li>
                <li><span style="color: #e74c3c;">2. <strong>Lack of Analytical Tools</strong></span>: Despite large volumes of data, there are no tools for analysis and decision-making indicators.</li>
                <li><span style="color: #e74c3c;">3. <strong>Redundancy and Waste</strong></span>: Data is often collected multiple times, wasting resources without adding value.</li>
                <li><span style="color: #e74c3c;">4. <strong>Diverse Expert Opinions</strong></span>: Experts have differing views on migration issues, requiring integration for a comprehensive understanding.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.write("""
        <h2 style="text-align: center; color: #e74c3c;">
            Proposed Big Data Solution
        </h2>
    """, unsafe_allow_html=True)
    
    st.write("""
        <div style="text-align: center;">
            <ul style="list-style-type: none;">
                <li><span style="color: #e74c3c;"><strong>Integration Framework</strong></span>: Develop a big data platform using Hadoop to integrate and visualize migration data.</li>
                <li><span style="color: #e74c3c;"><strong>Data Sources</strong></span>: Include data on climate, demography, geography, scientific evolution, soils, households, socio-economic activities, and administrative organization.</li>
                <li><span style="color: #e74c3c;"><strong>Technologies</strong></span>: Combine several migration databases and ontology databases.</li>
                <li><span style="color: #e74c3c;"><strong>Processing</strong></span>: Utilize the MapReduce paradigm for processing and visualization tools to display indicators and migration trends.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.write("""
        <h2 style="text-align: center; color: #e74c3c;">
            Goals
        </h2>
    """, unsafe_allow_html=True)

    st.write("""
        <div style="text-align: center;">
            <ul style="list-style-type: none;">
                <li><span style="color: #e74c3c;"><strong>Comprehensive Data Integration</strong></span>: Create a unified framework for acquiring and integrating migration data.</li>
                <li><span style="color: #e74c3c;"><strong>Enhanced Decision-Making</strong></span>: Provide tools for analyzing data and visualizing relevant decision indicators and recommendations.</li>
                <li><span style="color: #e74c3c;"><strong>Efficient Resource Use</strong></span>: Reduce redundancy and improve the value of collected data.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)




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


def create_migration_chart(data):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='From_Country', y='To_Country', data=data)
    plt.title('Migrations entre les pays de l\'Afrique de l\'Ouest')
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Fonction pour créer un diagramme en bâtons
def create_bar_chart(data):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=data['To_Country'], y=data['From_Country'])
    # sns.barplot(x=data['From_Country'], y=data['To_Country'], orient='h')
    plt.title('Diagramme en bâtons')
    st.pyplot(plt)

# Fonction pour créer un diagramme circulaire
def create_pie_chart(data):
    plt.figure(figsize=(8, 8))
    data['From_Country'].value_counts().plot.pie(autopct='%1.1f%%')
    plt.title('Diagramme circulaire')
    st.pyplot(plt)

# Fonction pour créer un histogramme
def create_histogram(data):
    plt.figure(figsize=(10, 6))
    sns.histplot(data['From_Country'], bins=30)
    plt.title('Histogramme')
    st.pyplot(plt)

# Fonction pour créer un nuage de points
def create_scatter_plot(data):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=data['From_Country'], y=data['To_Country'])
    plt.title('Nuage de points')
    st.pyplot(plt)



def afficher_details_fichier(file_id):
    fichier = metadata_collection.find_one({"_id": ObjectId(file_id)})
    
    if not fichier:
        st.error("Fichier non trouvé.")
        return
    
    st.header("Détails du fichier")
    
    # CSS styles for table and button
    st.markdown("""
        <style>
        .center-table { display: flex; justify-content: center; align-items: center; }
        .full-width-table { width: 100%; border-collapse: collapse; }
        .full-width-table th, .full-width-table td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        .full-width-table th { background-color: #f2f2f2; }
        .download-button { background-color: red; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer; margin: 10px 0; }
        </style>
    """, unsafe_allow_html=True)

    # Display file details in a table
    st.markdown(f"""
        <div class="center-table">
            <table class="full-width-table">
                <tr><th>Type de fichier</th><td>{fichier['type_fichier']}</td></tr>
                <tr><th>Auteur</th><td>{fichier['auteur']}</td></tr>
                <tr><th>Date de chargement</th><td>{fichier['date_chargement']}</td></tr>
                <tr><th>Description</th><td>{fichier['description']}</td></tr>
                <tr><th>Visibilité</th><td>{fichier['visibilite']}</td></tr>
            </table>
        </div>
    """, unsafe_allow_html=True)

    # Display data if available
    if "data" in fichier:
        df = pd.DataFrame(fichier["data"])
        # Visualization based on file type
        if fichier['type_fichier'] == "Migration Data":
            handle_migration_data_visualization(fichier)
        # Visualization based on file type
        if fichier['type_fichier'] == "Factors Data":
            # Handle Factors Data specific visualization
            handle_factors_data_visualization(fichier)
        elif fichier['type_fichier'] == "Spatiale Data":
            # Handle Spatial Data specific visualization
            handle_spatial_data_visualization(fichier)
        # df = pd.DataFrame(fichier["data"])
        
    
        # Download button for the CSV file
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger le fichier",
            data=csv,
            file_name=f"{fichier['auteur']}_{fichier['date_chargement']}.csv",
            mime='text/csv',
            help="Cliquez pour télécharger le fichier"
        )
        
        if st.button("Retour"):
            st.experimental_set_query_params()

    else:
        st.warning("Aucune donnée disponible pour ce fichier.")


def handle_factors_data_visualization(fichier):
    # Logic for handling Factors Data visualization
    df = pd.DataFrame(fichier["data"])  # Assuming data is in the same format

    # Sidebar for visualization options
    with st.sidebar:
        visualization_type = option_menu(
            'Choisir le type de visualisation:',
            ['Tabulaire', 'Bar Chart', 'Line Chart'],
            icons=['list', 'bar-chart', 'line-chart'],
            menu_icon="cast",
            default_index=0,
            orientation='vertical'
        )

    st.write(f'Vous avez sélectionné : {visualization_type}')

    if visualization_type == 'Tabulaire':
        st.dataframe(df)
    elif visualization_type == 'Bar Chart':
        st.bar_chart(df.set_index('year')[['valeur']])
    elif visualization_type == 'Line Chart':
        st.line_chart(df.set_index('year')[['valeur']])



def handle_migration_data_visualization(fichier):
    df = pd.DataFrame(fichier["data"])
        
    # Sidebar for visualization options
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
            st.dataframe(df)
    elif visualization_type == 'Bar Chart':
            st.bar_chart(df.set_index('Year')[['Migrants']])
    elif visualization_type == 'Line Chart':
            st.line_chart(df.set_index('Year')[['Migrants']])
    elif visualization_type == 'Area Chart':
            st.area_chart(df.set_index('Year')[['Migrants']])




def handle_spatial_data_visualization(fichier):
    # Assume 'data' is directly available in the 'fichier' object
    data = fichier.get('data')  # Access the data directly from the file

    if data is not None and len(data) > 0:
        # Convert to DataFrame if it's not already one
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)

        # Sidebar for visualization options
        with st.sidebar:
            selected = option_menu(
                menu_title=None,
                options=["Tabulaire", "Carte", "Circulaire", "Histogramme", "Nuage Points"],
                icons=["house", "map", "pie-chart", "bar-chart", "scatter-plot"],
                menu_icon="cast",
                default_index=0,
                orientation="vertical"
            )

        st.write(f'Vous avez sélectionné : {selected}')

        # Display based on selected visualization type
        if selected == "Tabulaire":
            st.dataframe(data)

        elif selected == "Carte":
            map_ = create_international_map(data)  # Replace with your map creation logic
            st.write("Carte des migrations:")
            folium_static(map_)  # Assuming folium_static is imported correctly

        elif selected == "Circulaire":
            st.write("Diagramme circulaire des migrations:")
            create_pie_chart(data)  # Function to create pie chart

        elif selected == "Histogramme":
            st.write("Histogramme des migrations:")
            create_histogram(data)  # Function to create histogram

        elif selected == "Nuage Points":
            st.write("Nuage de points des migrations:")
            create_scatter_plot(data)  # Function to create scatter plot

    else:
        st.warning("Aucune donnée disponible pour cette visualisation.")



# Function to update file details
def details_mettre_a_jour_fichier(file_id_up):
    fichier = metadata_collection.find_one({"_id": ObjectId(file_id_up)})
    
    if not fichier:
        st.error("Fichier non trouvé.")
        return
    
    query_params1 = st.experimental_get_query_params()
    file_id_up = query_params1.get("file_id_up")

    if file_id_up:
        fichier = metadata_collection.find_one({"_id": ObjectId(file_id_up[0])})
        
        if fichier:
            st.header("Update the selected file")
            
            # Prefill form fields with the file's current data
            type_fichier = st.text_input("Type de fichier", fichier.get("type_fichier", ""))
            auteur = st.text_input("Auteur", fichier.get("auteur", ""))
            description = st.text_area("Description", fichier.get("description", ""))
            date_chargement = st.date_input("Date de chargement", datetime.strptime(fichier["date_chargement"], "%Y-%m-%d"))
            date_fin = st.date_input("Date de fin", datetime.strptime(fichier.get("date_fin", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d"))
            visibilite = st.selectbox("Visibilité", ["Public", "Privé"], index=["Public", "Privé"].index(fichier.get("visibilite", "Public")))

            # Upload new data file
            uploaded_file = st.file_uploader("Choisir un fichier CSV ou Excel pour mise à jour", type=["csv", "xlsx"])
            if uploaded_file is not None:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                # Check for required columns
                required_columns = ["Year", "Migrants"]  # Example required columns
                if all(column in df.columns for column in required_columns):
                    st.success("Le fichier contient toutes les colonnes requises.")
                    
                    if st.button("Mettre à jour"):
                        # Update document in MongoDB
                        metadata_collection.update_one(
                            {"_id": ObjectId(file_id_up[0])},
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
            else:
                if st.button("Mettre à jour sans changer de fichier"):
                    # Update metadata only, without new file
                    metadata_collection.update_one(
                        {"_id": ObjectId(file_id_up[0])},
                        {"$set": {
                            "type_fichier": type_fichier,
                            "auteur": auteur,
                            "description": description,
                            "date_chargement": date_chargement.strftime("%Y-%m-%d"),
                            "date_fin": date_fin.strftime("%Y-%m-%d"),
                            "visibilite": visibilite
                        }}
                    )
                    st.success("Fichier mis à jour avec succès!")
                if st.button("Retour"):
                    st.experimental_set_query_params()



# Function to list all files in MongoDB with an update link
def list_files_to_update():
    fichiers = list(metadata_collection.find())
    fichiers_df = pd.DataFrame(fichiers, columns=["_id", "type_fichier", "auteur", "date_chargement", "description", "visibilite"])

    # Convert ObjectId to string for display
    fichiers_df["_id"] = fichiers_df["_id"].apply(str)

    # Create an "Update" link with the file ID in the query string
    fichiers_df['Update'] = fichiers_df["_id"].apply(
        lambda id: f'<a href="?file_id_up={id}" target="_self" class="update-link">📝 Update</a>'
    )
    

    # Display the table with custom styling and HTML links
    st.write("""
        <div class="table-container">
            {table}
        </div>
    """.format(table=fichiers_df[['type_fichier', 'auteur', 'date_chargement', 'description', 'visibilite', 'Update']].to_html(escape=False, index=False)), unsafe_allow_html=True)

    # CSS for styling the table and update links
    st.markdown(
        """
        <style>
        .table-container {
            margin: 25px 0;
            font-size: 18px;
            min-width: 400px;
        }
        .table-container table {
            width: 100%;
            border-collapse: collapse;
        }
        .table-container th, .table-container td {
            padding: 12px 15px;
            border: 1px solid #ddd;
        }
        .table-container th {
            background-color: #009879;
            color: #ffffff;
            text-align: center;
        }
        .table-container td {
            text-align: center;
        }
        .table-container tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }
        .table-container tr:hover {
            background-color: #f1f1f1;
        }
        .update-link {
            color: #007bff;
            text-decoration: none;
            font-weight: bold;
        }
        .update-link:hover {
            color: #0056b3;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    query_params = st.experimental_get_query_params()
    if "file_id_up" in query_params:
        details_mettre_a_jour_fichier(query_params["file_id_up"][0])



def liste_fichiers():
    st.subheader("Available Dataset")
    st.write("""
        <div style="background-color: #3498db; padding: 7px;">
            <h3 style="color: white; text-align: center;">
                View Different Data from institutions and researchers around the world
            </h3>
        </div>
    """, unsafe_allow_html=True)

    # Retrieve all files from the collection
    fichiers = list(metadata_collection.find())

    # Convert the list of files into a DataFrame
    fichiers_df = pd.DataFrame(fichiers, columns=["_id", "type_fichier", "auteur", "date_chargement", "description", "visibilite"])

    # Remove the MongoDB ObjectId for simplicity in display
    fichiers_df["_id"] = fichiers_df["_id"].apply(str)

    # Create a column with "Voir détails" links using HTML and query parameters
    fichiers_df['Voir détails'] = fichiers_df["_id"].apply(
        lambda id: f'<a href="?file_id={id}" target="_self" class="details-link">🔍Voir détails</a>'
    )

    # Display the table using st.write with the HTML-rendered links
    st.write("""
        <div class="table-container">
            {table}
        </div>
    """.format(table=fichiers_df[['type_fichier', 'auteur', 'date_chargement', 'description', 'visibilite', 'Voir détails']].to_html(escape=False, index=False)), unsafe_allow_html=True)

    # Add the CSS for styling
    st.markdown(
        """
        <style>
        .table-container {
            display: flex;
            justify-content: center;
            margin: 20px;
        }
        .table-container table {
            border-collapse: collapse;
            width: 100%;
            margin: 25px 0;
            font-size: 18px;
            min-width: 400px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        }
        .table-container th, .table-container td {
            padding: 12px 15px;
        }
        .table-container th {
            background-color: #009879;
            color: #ffffff;
            text-align: center;
        }
        .table-container td {
            text-align: center;
            border-bottom: 1px solid #dddddd;
        }
        .table-container tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }
        .table-container tr:hover {
            background-color: #f1f1f1;
        }
        .details-link {
            color: #007bff;
            text-decoration: none;
            font-weight: bold;
        }
        .details-link:hover {
            color: #0056b3;
        }
        </style>
        """,
        unsafe_allow_html=True
    )





def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Connexion",
            options=["Welcome", "View Data","Request","Sign In"],
            icons=["house","table","database","box-arrow-in-right"],
            default_index=1,  # Set default to "Welcome"
            orientation="vertical"
        )
    return selected

  

# def logout():
#     if st.button("Disconnect"):
#         try:
#             keycloak.authenticated = False  # Disconnect
#             st.rerun()  # Redirect to the homepage
#             # st.experimental_rerun()  # Reload the interface
#         except Exception as e:
#             st.error(f"An error occurred: {e}")

# def logout():
#     keycloak.logout(redirect_uri='http://localhost:8501/')  # Redirection vers une page Streamlit
#     st.success('Vous êtes maintenant déconnecté.')
           
# def logout():
#     try:
#         keycloak.logout(redirect_uri='http://localhost:8501/')
#         st.success("Logged out successfully!")
#     except Exception as e:
#         st.error(f"Logout failed: {str(e)}")


    
# def logout():
#     logout_url = "http://localhost:8080/realms/humanmigration/protocol/openid-connect/logout?redirect_uri=http://localhost:8501/"
#     st.write(f"Redirecting to: {logout_url}")
#     js = f"window.location.href = '{logout_url}'"
#     keycloak.authenticated = False
#     st.markdown(f"<script>{js}</script>", unsafe_allow_html=True)



import streamlit as st
from keycloak import KeycloakOpenID

# Configuration de Keycloak
keycloak = KeycloakOpenID(
    server_url="http://localhost:8080/",
    client_id="humanmigration",
    realm_name="humanmigration"
)

# Vérifie si l'utilisateur est authentifié
def is_authenticated():
    return st.session_state.get("authenticated", False)

# Fonction de connexion
def login_user(username, password):
    try:
        token = keycloak.token(username, password)
        st.session_state["authenticated"] = True
        st.session_state["token"] = token
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")

# Fonction de déconnexion
def logout_user():
    st.session_state["authenticated"] = False
    st.session_state.pop("token", None)


def welcome_msg():
    
    query_params = st.experimental_get_query_params()

    # Check if the "file_id" is present to show file details
    if "file_id" in query_params:
        file_id = query_params["file_id"][0]
        afficher_details_fichier(file_id)  # Show file details

    # Check if the "file_id_up" is present to show file update form
    elif "file_id_up" in query_params:
        file_id_up = query_params["file_id_up"][0]
        details_mettre_a_jour_fichier(file_id_up)  # Show update form

    else:
        selected_option = sidebar_menu()
        
        if selected_option == "View Data":
            liste_fichiers()
            charger_fichier()
        elif selected_option == "Welcome":
            display_welcome_page()
        elif selected_option =="Request":
            # st.write("Requesting data")
            home_request()
        elif selected_option== "Sign In":
            # Bouton pour afficher le formulaire de connexion
            keycloak = login(
                    url="http://localhost:8080",
                    realm="humanmigration",
                    client_id="humanmigration",
                )
            # if st.button("Disconnect"):
            #     keycloak.authenticated = False
            
            if st.button("Se connecter"):
                st.session_state["show_login"] = True
                # st.experimental_rerun()

            

# Affiche le message de bienvenue ou le formulaire de connexion
if not is_authenticated():
    if st.session_state.get("show_login", False):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        
        if st.button("Se connecter"):
            login_user(username, password)
            # st.experimental_rerun()  # Rafraîchir pour mettre à jour l'état
    else:
        welcome_msg()
else:
    # Menu dans la barre latérale
    menu_options = ["Welcome dashboard", "Load Data", "Update Data", "Delete Data", "🔍 API", "🔍 Prediction", "Logout"]

    with st.sidebar:
        choix = option_menu(
            "Menu", 
            menu_options,
            icons=["house", "cloud-upload", "pencil", "trash", "book", "file-bar-graph-fill", "box-arrow-in-right"],
            menu_icon="cast",
            default_index=0,
            orientation='vertical'
        )

    # Logique en fonction du choix du menu
    if choix == "Welcome dashboard":
        home_admin()
    elif choix == "Load Data":
        charger_fichier()
    elif choix == "Update Data":
        list_files_to_update()
    elif choix == "Delete Data":
        list_files_to_delete()
    elif choix == "🔍 API":
        open_api_migrate()
    elif choix == "🔍 Prediction":
        # st.write("Prédiction")
        main()
    elif choix == "Logout":
        logout_user()
        # st.experimental_rerun()  # Rafraîchir pour mettre à jour l'état
