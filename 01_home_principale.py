import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from bson.objectid import ObjectId
from streamlit_option_menu import option_menu
from PIL import Image
from dataclasses import asdict
from streamlit_keycloak import login
import streamlit as st
from home_admin_01 import home_admin
from factors_data import consult_data, charger_fichier_factors
from spatiale import consulation_spatiale,upload_file_spatiale 
from api_ui import open_api_migrate
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning) 

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['test1_db']
metadata_collection = db['metadata']



# ****************************************************************************************
# *****************************************************************************************
# # This is the global part to be appear in all page. It's follow with marque css design
# # Configuration de la page


st.set_page_config(page_title="Migration Data Hub",page_icon="🌍", layout="wide")
import os

# st.set_option('deprecation.showfileUploaderEncoding', False)
# st.set_option('deprecation.showPyplotGlobalUse', False)

# os.environ['PYTHONWARNINGS'] = "ignore::DeprecationWarning"
# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# import streamlit as st
# import warnings

# # Suppress specific deprecation warning
# warnings.filterwarnings("ignore", message="Please replace st.experimental_get_query_params with st.query_params.")

# import streamlit as st
# import sys
# import os
# # Temporarily suppress stderr to hide the deprecation message
# stderr = sys.stderr
# sys.stderr = open(os.devnull, "w")

# # Use st.experimental_get_query_params temporarily without warning
# params = st.experimental_get_query_params()

# # Restore stderr
# sys.stderr = stderr






 


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



def main():
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
    main()
else:
    st.write("Sign In !")




# Colonnes requises
required_columns = ['Year', 'Location', 'Origin', 'Region', 'Investment', 'Type', 'Destination', 'Age Group', 'Education Level', 'Rating', 'Migrants', 'raisons']

# Fonctionnalité 1: Charger un fichier
def charger_fichier():
    st.header("Charger un fichier")
    uploaded_file = st.file_uploader("Choisir un fichier CSV ou Excel", type=["csv", "xlsx"])

    type_fichier = st.selectbox("Data type",["Migration Data","Spatiale Data", "Factors Data"])

    # if type_fichier == "Factors Data":
    #     charger_fichier_factors()
    if type_fichier == "Spatiale Data":
        upload_file_spatiale()
    else:

        auteur = st.text_input("Auteur")
        description = st.text_area("Description")
        date_chargement = st.date_input("Date de chargement", datetime.now())
        date_fin = st.date_input("Date de fin")
        visibilite = st.selectbox("Visibilité", ["Public", "Privé"])
        
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Vérifier si les colonnes requises sont présentes
            if all(column in df.columns for column in required_columns):
                st.success("Le fichier contient toutes les colonnes requises.")
                              
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
        consulation_spatiale()
    elif file_option == 'Factors Data':
        consult_data()
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
    image = Image.open("img5.jpg")

    # Title and slogan
    st.markdown("<h1 style='text-align: center; color: #004d99;'>Migration Data Hub</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #0066cc;'>Your portal to explore, analyze and visualize migration data.</h2>", unsafe_allow_html=True)
    
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
    # st.header("Challenges")
    st.write("""
        <div style="text-align: center;">
            1. <span style="color: #e74c3c;">**Data Fragmentation**</span>: Researchers collect data in various formats and for different purposes, leading to fragmented information.
            2. <span style="color: #e74c3c;">**Lack of Analytical Tools**</span>: Despite the large volumes of data, there are no tools to analyze and provide decision-making indicators, recommendations, and predictions.
            3. <span style="color: #e74c3c;">**Redundancy and Waste**</span>: Data is often collected multiple times, wasting time and resources without adding value.
            4. <span style="color: #e74c3c;">**Diverse Expert Opinions**</span>: Experts have differing views on migration issues, which need to be integrated for a comprehensive understanding.</br>
        </div>
    """, unsafe_allow_html=True)


    st.write("""
        <h2 style="text-align: center; color: #e74c3c;">
            Proposed Big Data Solution
        </h2>
    """, unsafe_allow_html=True)
    

    
    # st.header("Proposed Big Data Solution") 
    st.write("""
        <div style="text-align: center;">
            - <span style="color: #e74c3c;">Integration Framework</span>: Develop a big data platform using Hadoop to integrate and visualize migration data.
            - <span style="color: #e74c3c;">Data Sources</span>: Include data on climate, demography, geography, scientific evolution, soils, households, socio-economic activities, and administrative organization.
            - <span style="color: #e74c3c;">Technologies</span>: Combine several migration databases and ontology databases.
            - <span style="color: #e74c3c;">Processing</span>: Utilize MapReduce paradigm for processing and visualization tools to display indicators and migration trends.
        </div>
    """, unsafe_allow_html=True)


    st.write("""
        <h2 style="text-align: center; color: #e74c3c;">
            Goals
        </h2>
    """, unsafe_allow_html=True)

    # st.header("Goals")
    st.write("""
        <div style="text-align: center;">
            <span style="color: #e74c3c;">Comprehensive Data Integration</span>: Create a unified framework for acquiring and integrating migration data.
            <span style="color: #e74c3c;">Enhanced Decision-Making</span>: Provide tools for analyzing data and visualizing relevant decision indicators and recommendations.
            <span style="color: #e74c3c;">Efficient Resource Use</span>: Reduce redundancy and improve the value of collected data. <br><br><br><br><br>
        </div>
    """, unsafe_allow_html=True)





def afficher_details_fichier(file_id):
    fichier = metadata_collection.find_one({"_id": ObjectId(file_id)})
    if fichier:
        st.header("Détails du fichier")
        
        # CSS pour centrer le tableau et occuper toute la page
        st.markdown("""
            <style>
            .center-table {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }
            .full-width-table {
                width: 100%;
                border-collapse: collapse;
            }
            .full-width-table th, .full-width-table td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }
            .full-width-table th {
                background-color: #f2f2f2;
            }
            .download-button {
                background-color: red;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-align: center;
                display: inline-block;
                margin: 10px 0;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Détails du fichier dans un tableau
        st.markdown(f"""
            <div class="center-table">
                <table class="full-width-table">
                    <tr><th>File Type</th><td>{fichier['type_fichier']}</td></tr>
                    <tr><th>Othor</th><td>{fichier['auteur']}</td></tr>
                    <tr><th>Load Date</th><td>{fichier['date_chargement']}</td></tr>
                    <tr><th>Description</th><td>{fichier['description']}</td></tr>
                    <tr><th>Visibility</th><td>{fichier['visibilite']}</td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
        
        df = pd.DataFrame(fichier["data"])
        # st.write(df)
        


        fichiers = list(metadata_collection.find())
        df = pd.DataFrame(fichiers)

        # Supprimer les colonnes 'description', 'visibilite', 'data', '_id'
        df = df.drop(columns=['description', 'visibilite', 'data', '_id'])
        # Créer les fichier_ids
        fichier_ids = [(f"{fichier.get('auteur', 'inconnu')}_{datetime.now().year}_{index:04d}", str(fichier["_id"])) 
                    for index, fichier in enumerate(fichiers, start=1)]

        # Afficher les boutons radio pour chaque fichier
        # fichier_choisi = st.radio("Choisir", fichier_ids, format_func=lambda x: x[0])
        # Ajouter la colonne 'view' avec fichier_ids
        df['view'] = [f"Details for {fichier[0]}" for fichier in fichier_ids]

        # # Afficher le DataFrame sans ces colonnes
        # st.dataframe(df)


        # Process the selected file
       
        if fichier and "data" in fichier:
            df = pd.DataFrame(fichier["data"])
                # st.write(f"Données pour le fichier {fichier_choisi[0]}:")
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

        # Bouton de téléchargement
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger le fichier",
            data=csv,
            file_name=f"{fichier['auteur']}_{fichier['date_chargement']}.csv",
            mime='text/csv',
            key='download-csv',
            help="Cliquez pour télécharger le fichier"
        )
        
        # CSS pour styliser le bouton de téléchargement
        st.markdown("""
            <style>
            .stDownloadButton button {
                background-color: red;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-align: center;
                display: inline-block;
                margin: 10px 0;
            }
            </style>
        """, unsafe_allow_html=True)
        
        if st.button("Retour"):
            st.experimental_set_query_params()


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
        lambda id: f'<a href="?file_id={id}" target="_self">Voir détails</a>'
    )

    # Display the table using st.write with the HTML-rendered links
    st.write("""
        <div style="display: flex; justify-content: center; margin: 20px;">
            {table}
        </div>
    """.format(table=fichiers_df[['type_fichier', 'auteur', 'date_chargement', 'description', 'visibilite', 'Voir détails']].to_html(escape=False)), unsafe_allow_html=True)



# def liste_fichiers_factors():
#     st.subheader("Available Dataset")
#     st.write("""
#         <div style="background-color: #3498db; padding: 7px;">
#             <h3 style="color: white; text-align: center;">
#                 View Different Data from institutions and researchers around the world
#             </h3>
#         </div>
#     """, unsafe_allow_html=True)

#     # Retrieve all files from the collection
#     fichiers = list(metadata_collection.find())
    
#     # Convert the list of files into a DataFrame
#     fichiers_df = pd.DataFrame(fichiers, columns=["_id", "type_fichier", "auteur", "date_chargement", "description", "visibilite"])

#     # Remove the MongoDB ObjectId for simplicity in display
#     fichiers_df["_id"] = fichiers_df["_id"].apply(str)

#     # Create a column with "Voir détails" links using HTML and query parameters
#     fichiers_df['Voir détails'] = fichiers_df["_id"].apply(
#         lambda id: f'<a href="?file_id={id}" target="_self">Voir détails</a>'
#     )

#     # Display the table using st.write with the HTML-rendered links
#     st.write("""
#         <div style="display: flex; justify-content: center; margin: 20px;">
#             {table}
#         </div>
#     """.format(table=fichiers_df[['type_fichier', 'auteur', 'date_chargement', 'description', 'visibilite', 'Voir détails']].to_html(escape=False)), unsafe_allow_html=True)

def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Connexion",
            options=["View Data", "Welcome", "Consultation"],
            icons=["house", "person", "table", "file-text"],
            default_index=1,  # Set default to "Welcome"
            orientation="vertical"
        )
    return selected



def welcome_msg():
    # # Suppress specific deprecation warning
    # warnings.filterwarnings("ignore", message="Please replace st.experimental_get_query_params with st.query_params.")
    
    query_params = st.experimental_get_query_params()
    if "file_id" in query_params:
        file_id = query_params["file_id"][0]
        afficher_details_fichier(file_id)
    else:
        selected_option = sidebar_menu()
        
        if selected_option == "Welcome":
            display_welcome_page()
        elif selected_option == "View Data":
            liste_fichiers()
        elif selected_option == "Consultation":
            consulter_donnees()

# Appel de la fonction
if not keycloak.authenticated:
    welcome_msg()


# Sidebar menu options
menu_options = ["Welcome dashboard", "Consulter les données", "Consulter métadonnées","Migration factors","🔍 API","🔍Prediction"]

# Add options based on authentication
if keycloak.authenticated:
    menu_options.insert(1, "Charger un fichier")
    menu_options.insert(2, "Mettre à jour un fichier")
    menu_options.insert(3, "Supprimer un fichier")

# Sidebar menu
if keycloak.authenticated:
    with st.sidebar:
        choix = option_menu(
            "Menu", 
            menu_options,
            icons=["house", "cloud-upload", "pencil", "trash", "table","table", "info-circle"] if keycloak.authenticated else ["house", "table","table","table", "info-circle"],
            menu_icon="cast",
            default_index=0,
            orientation='vertical'
        )

    # Functionality based on menu selection
    if choix == "Welcome dashboard":
        home_admin()
    elif choix == "Charger un fichier" and keycloak.authenticated:
        charger_fichier()
    elif choix == "Mettre à jour un fichier" and keycloak.authenticated:
        mettre_a_jour_fichier()
    elif choix == "Supprimer un fichier" and keycloak.authenticated:
        supprimer_fichier()
    elif choix == "Consulter les données":
        consulter_donnees()
    elif choix == "Consulter métadonnées":
        consulter_metadata()
    elif choix == "Migration factors":
        charger_fichier_factors()
    elif choix == "🔍 API":
        open_api_migrate()
    elif choix == "🔍Prediction":
        st.write("Predit")
