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



# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['test_finale_db']
metadata_collection = db['metadata']


# Define required columns for different data types
required_columns_mapping = {
    "Migration Data": ['Year', 'Location', 'Origin', 'Region', 'Investment', 'Type', 'Destination', 'Age Group', 'Education Level', 'Rating', 'Migrants', 'raisons'],
    "Factors Data": ['year', 'factor', 'type', 'location', 'valeur'],
    "Spatiale Data": ['Year', 'From_Country', 'To_Country', 'Migrants', 'Latitude_From', 'Longitude_From','Latitude_To', 'Longitude_To']
}

# Function to load file to MongoDB
def charger_fichier_up():
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

# Function to list all files in MongoDB
def list_files():
    fichiers = list(metadata_collection.find())
    fichiers_df = pd.DataFrame(fichiers, columns=["_id", "type_fichier", "auteur", "date_chargement", "description", "visibilite"])

    # Remove the MongoDB ObjectId for simplicity in display
    fichiers_df["_id"] = fichiers_df["_id"].apply(str)

    # Create a column with "View Details" links using HTML
    fichiers_df['View Details'] = fichiers_df["_id"].apply(
        lambda id: f'<a href="?file_id={id}" target="_self">View Details</a>'
    )

    # Display the table using st.write with the HTML-rendered links
    st.write("""
        <div style="display: flex; justify-content: center; margin: 20px;">
            {table}
        </div>
    """.format(table=fichiers_df[['type_fichier', 'auteur', 'date_chargement', 'description', 'visibilite', 'View Details']].to_html(escape=False)), unsafe_allow_html=True)


# list_files()
# charger_fichier_up()


import pandas as pd
import streamlit as st
from bson import ObjectId
from datetime import datetime

import streamlit as st
import pandas as pd

# Function to list all files in MongoDB with a delete link
def list_files_to_delete():
    fichiers = list(metadata_collection.find())
    fichiers_df = pd.DataFrame(fichiers, columns=["_id", "type_fichier", "auteur", "date_chargement", "description", "visibilite"])

    # Convert the MongoDB ObjectId to string for display
    fichiers_df["_id"] = fichiers_df["_id"].apply(str)

    # Add "Delete" links in the table for each file
    fichiers_df['Delete'] = fichiers_df["_id"].apply(
        lambda file_id: f'<a href="?delete_id={file_id}" class="delete-link" target="_self">Delete</a>'
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



# Function to list all files in MongoDB with a delete icon
def list_files():
    fichiers = list(metadata_collection.find())
    fichiers_df = pd.DataFrame(fichiers, columns=["_id", "type_fichier", "auteur", "date_chargement", "description", "visibilite"])

    # Convert the MongoDB ObjectId to string for display
    fichiers_df["_id"] = fichiers_df["_id"].apply(str)

    # Add "Delete" links with a trash can icon
    fichiers_df['Delete'] = fichiers_df["_id"].apply(
        lambda file_id: f'<a href="?delete_id={file_id}" target="_self" style="text-decoration: none; color: red;">🗑️ Delete</a>'
    )

    # Display the table with HTML-rendered links
    st.write(fichiers_df[['type_fichier', 'auteur', 'date_chargement', 'description', 'visibilite', 'Delete']].to_html(escape=False), unsafe_allow_html=True)

# Function to delete a file when a file ID is in the URL query parameters
# Function to delete a file when a file ID is in the URL query parameters
def supprimer_fichier():
    # Check if 'delete_id' is in query parameters
    query_params = st.experimental_get_query_params()
    delete_id = query_params.get("delete_id")

    if delete_id:
        # Delete the file by ID
        metadata_collection.delete_one({"_id": ObjectId(delete_id[0])})
        st.success("Fichier supprimé avec succès!")

        # Clear the query parameter to prevent repeated deletion on refresh
        st.experimental_set_query_params()

# # Streamlit layout to display list and delete files
# st.header("List of Files")
# list_files_to_delete()
# supprimer_fichier()




import streamlit as st
import pandas as pd
from datetime import datetime
from bson import ObjectId

# Function to list all files in MongoDB with an update link
def list_files_to_update():
    fichiers = list(metadata_collection.find())
    fichiers_df = pd.DataFrame(fichiers, columns=["_id", "type_fichier", "auteur", "date_chargement", "description", "visibilite"])

    # Convert ObjectId to string for display
    fichiers_df["_id"] = fichiers_df["_id"].apply(str)

    # Create an "Update" link with the file ID in the query string
    fichiers_df['Update'] = fichiers_df["_id"].apply(
        lambda id: f'<a href="?file_id={id}" target="_self" class="update-link">📝 Update</a>'
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

# Function to update file details
def details_mettre_a_jour_fichier(file_id):
    fichier = metadata_collection.find_one({"_id": ObjectId(file_id)})
    
    if not fichier:
        st.error("Fichier non trouvé.")
        return
    
    query_params = st.experimental_get_query_params()
    file_id = query_params.get("file_id")

    if file_id:
        fichier = metadata_collection.find_one({"_id": ObjectId(file_id[0])})
        
        if fichier:
            st.header("Mettre à jour le fichier sélectionné")
            
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
                            {"_id": ObjectId(file_id[0])},
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
                        {"_id": ObjectId(file_id[0])},
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

# Pour tester la liste des fichiers à mettre à jour
charger_fichier_up()
# Tester la mise à jour des détails du fichier si un ID de fichier est fourni
query_params = st.experimental_get_query_params()
if "file_id" in query_params:
    details_mettre_a_jour_fichier(query_params["file_id"][0])
else:
    st.write("bienvenue")



# Display the file list and enable updates
# st.header("Liste des fichiers")
# list_files_to_update()
# details_mettre_a_jour_fichier()



