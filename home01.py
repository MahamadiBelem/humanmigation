import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import bcrypt
from streamlit_option_menu import option_menu
from io import StringIO
from PIL import Image
import plotly.express as px
from streamlit_option_menu import option_menu
import os
from archive.data_management import main
from archive.main_app_map import main2
from prediction import predict_migrant
from archive.visualisation import visualize
from api_ui import open_api_migrate
from bson import ObjectId
# from fix_colums import consulter_donnees


# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['16092024']
collection = db['maincollection']
metadata_collection = db['mainmetadata']
users_collection = db['mainusers']



# ****************************************************************************************
# *****************************************************************************************

# Return a Id that is the concatenation 
# of USERNAME-YEAR-LAST_ORDER_NUMBER
def generate_file_id(username):
    year = datetime.now().year
    last_metadata = metadata_collection.find({"author": username}).sort("_id", -1).limit(1)
    
    last_order_number = 1
    try:
        last_doc = last_metadata.next()
        last_order_number = int(last_doc['_id'].split('-')[-1]) + 1
    except StopIteration:
        pass
    
    return f"{username}-{year}-{last_order_number}"

# ****************************************************************************************
# *****************************************************************************************

# Enable to laod data to mongoDB as documents with the require parameters: file, file_type,
# description, author, source, data_type, start_date, end_date
def load_data_to_mongo(file, file_type, description, author, source, data_type, start_date, end_date):
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())

    file_id = generate_file_id(author)

    try:
        if file_type == 'csv':
            df = pd.read_csv(file, encoding='utf-8-sig')
        elif file_type == 'excel':
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type")
            return
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        return

    df['file_id'] = file_id

    try:
        collection.insert_many(df.to_dict('records'))
    except Exception as e:
        st.error(f"Error inserting data into MongoDB: {e}")
        return

    metadata = {
        '_id': file_id,
        'description': description,
        'author': author,
        'date_loaded': datetime.now(),
        'source': source,
        'data_type': data_type,
        'file_type': file_type,
        'start_date': start_datetime,
        'end_date': end_datetime
    }
    try:
        metadata_collection.insert_one(metadata)
        st.success("Data successfully uploaded to MongoDB")
    except Exception as e:
        st.error(f"Error inserting metadata into MongoDB: {e}")

# ****************************************************************************************
# *****************************************************************************************



# delete a by precising his name
def delete_file(file_id):
    try:
        collection.delete_many({'file_id': file_id})
        metadata_collection.delete_one({'_id': file_id})
        st.success("File successfully deleted")
    except Exception as e:
        st.error(f"Error deleting file: {e}")

# ****************************************************************************************
# *****************************************************************************************

# create a user and login by providing the require field
def create_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({"username": username, "password": hashed})

def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return True
    return False

# ****************************************************************************************
# *****************************************************************************************

def delete_data_from_mongo(doc_id):
    try:
        collection.delete_one({'_id': doc_id})
        st.success("Data successfully deleted")
    except Exception as e:
        st.error(f"Error deleting data: {e}")

# ****************************************************************************************
# *****************************************************************************************
# update with the require colums
def upload_by_update(file):
    try:
        df = pd.read_csv(file, encoding='utf-8-sig')
        
        required_columns = ['Year', 'Location', 'Origin', 'Region', 'Investment', 'Type', 'Destination', 'Age Group', 'Education Level', 'Rating', 'Migrants', 'raisons']
        if not all(col in df.columns for col in required_columns):
            st.error(f"File must contain the following columns: {', '.join(required_columns)}")
            return

        file_id = generate_file_id('admin')
        df['file_id'] = file_id

        records = df.to_dict('records')

        filter_criteria = {col: {'$in': df[col].tolist()} for col in required_columns}
        collection.delete_many(filter_criteria)
        
        collection.insert_many(records)
        st.success("Data successfully updated from the file")
        
    except Exception as e:
        st.error(f"Error updating data from the file: {e}")

# ****************************************************************************************
# *****************************************************************************************

# This home is the home after login succesfullly
def home3():
    # Chargement de l'image de fond
    image = Image.open("img2.jpeg")

    # Titre et slogan
    st.markdown("<h1 style='text-align: center; color: #004d99;'>Migration Data Hub</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #0066cc;'>Votre portail pour explorer, analyser et visualiser les données migratoires.</h2>", unsafe_allow_html=True)

    # Menu de navigation
    menu = st.sidebar.selectbox("Autres", ["À propos", "Contact"])

    # Section principale avec l'image de fond
    st.image(image, use_column_width=True)
    st.markdown("""
        <style>
        .main {background-color: #f0f2f6; padding: 20px;}
        .cta-button {background-color: #0066cc; color: white; padding: 10px 20px; border-radius: 5px; text-align: center; display: block; margin: 20px auto;}
        </style>
        """, unsafe_allow_html=True)

    # Appel à l'action
    if st.button("Commencez maintenant", key='cta'):
        st.markdown("<p style='text-align: center;'><a href='https://youraccountcreationlink.com' class='cta-button'>Créez votre compte</a></p>", unsafe_allow_html=True)

    # Présentation des fonctionnalités
    st.markdown("""
        <h3>Présentation des Fonctionnalités</h3>
        <ul>
            <li><strong>Charger des Données :</strong> Importez vos données en toute simplicité.</li>
            <li><strong>Consulter les Données Publiques :</strong> Accédez à une vaste base de données publiques.</li>
            <li><strong>Modifier les Données :</strong> Mettez à jour et corrigez vos données.</li>
            <li><strong>Faire des Requêtes :</strong> Interrogez les données pour obtenir des insights précis.</li>
            <li><strong>Visualiser les Données :</strong> Créez des visualisations interactives.</li>
            <li><strong>Télécharger des Données :</strong> Exportez les données pour une utilisation hors ligne.</li>
        </ul>
        """, unsafe_allow_html=True)

    # Témoignages et avis
    st.markdown("""
        <h3>Témoignages et Avis</h3>
        <p><strong>Témoignages d’Utilisateurs :</strong> Découvrez ce que nos utilisateurs disent de nous.</p>
        <p><strong>Évaluations :</strong> Note moyenne : 4.8/5</p>
        """, unsafe_allow_html=True)

    # Mises à jour et actualités
    st.markdown("""
        <h3>Mises à Jour et Actualités</h3>
        <p><strong>Dernières Nouvelles :</strong> Restez informé des dernières mises à jour et actualités sur les migrations.</p>
        """, unsafe_allow_html=True)

    # Style additionnel
    st.markdown("""
        <style>
        body {font-family: Arial, sans-serif;}
        h1 {font-size: 2.5em; color: #004d99;}
        h2 {font-size: 1.5em; color: #0066cc;}
        h3 {font-size: 1.2em; color: #003366;}
        </style>
        """, unsafe_allow_html=True)
#*****************************************************************************************
#*****************************************************************************************

import streamlit as st
import pandas as pd
from bson import ObjectId



def display_homepage():
    st.subheader("Available Dataset")
    st.write("""
        <div style="background-color: #3498db; padding: 7px;">
            <h3 style="color: white; text-align: center;">
                View Different Data from institutions and researchers around the world
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Fetch metadata from MongoDB
    metadata = list(metadata_collection.find())
    
    if metadata:
        # Create DataFrame from metadata
        df_metadata = pd.DataFrame(metadata)
        
        # Select relevant columns for display
        df_metadata = df_metadata[['description', 'author', '_id']]
        
        # Add "View Details" button as HTML links
        df_metadata['View Details'] = df_metadata['_id'].apply(
            lambda x: f'<a href="javascript:void(0);" onclick="viewDetails(\'{x}\')">View Details</a>'
        )
        
        # Generate HTML table
        html_table = df_metadata.to_html(escape=False, index=False)
        
        # Display the HTML table
        st.write(html_table, unsafe_allow_html=True)
        
        # Add JavaScript for button handling
        st.markdown("""
        <script>
        function viewDetails(file_id) {
            const queryParams = new URLSearchParams(window.location.search);
            queryParams.set('file_id', file_id);
            window.location.search = queryParams.toString();
        }
        </script>
        """, unsafe_allow_html=True)
    
    # Handle file detail display if file_id is in query params
    query_params = st.query_params
    if "file_id" in query_params:
        file_id = query_params["file_id"][0]
        if ObjectId.is_valid(file_id):  # Validate ObjectId
            afficher_details_fichier(file_id)
        else:
            st.error("Invalid file ID.")
    else:
        st.write("Select a file to view its details by clicking 'View Details'.")

def afficher_details_fichier(file_id):
    st.header("File Details")
    
    # Fetch the file metadata from MongoDB
    try:
        fichier = metadata_collection.find_one({"_id": ObjectId(file_id)})
    except Exception as e:
        st.error(f"Error fetching file: {e}")
        return
    
    if fichier:
        # Display the metadata
        st.subheader("File Metadata")
        st.write(f"**Author:** {fichier.get('author', 'N/A')}")
        st.write(f"**Description:** {fichier.get('description', 'N/A')}")
        st.write(f"**Start Date:** {pd.to_datetime(fichier.get('start_date', 'N/A')).strftime('%Y-%m-%d')}")
        
        # Option to display file data (optional)
        if st.checkbox("Show file data"):
            df = pd.DataFrame(fichier.get('data', []))
            st.dataframe(df)
    else:
        st.error("File not found.")




# ****************************************************************************************
# ****************************************************************************************
# This home the home for all user. No login is need to that
def display_homepage1():
    st.subheader("Available Dataset")
    st.write("""
                    <div style="background-color: #3498db; padding: 7px;">
                        <h3 style="color: white; text-align: center;">
                            View Different  Data from institutions and researchers from the world
                        </h3>
                    </div>
                """, unsafe_allow_html=True)
    
    # Fetch metadata from MongoDB
    metadata = list(metadata_collection.find())
    
    if metadata:
        # Create DataFrame from metadata
        df_metadata = pd.DataFrame(metadata)

        def highlight_rows(row):
            return ['background-color: #f2f2f2' if row.name % 2 == 0 else 'background-color: #ffffff'] * len(row)
    
        # Style the DataFrame
        df_styled = df_metadata.style.set_properties(**{
            'font-family': 'Times New Roman',
        }).apply(highlight_rows, axis=1)
        
        # Display the styled DataFrame***************
        st.dataframe(df_styled)

        # Allow user to select a file description
        selected_description = st.selectbox("Select a file description", df_metadata['description'])
        
        if selected_description:
            # Filter metadata based on selected description
            selected_metadata = df_metadata[df_metadata['description'] == selected_description].iloc[0]
            selected_file_id = selected_metadata['_id']
            
            # Create DataFrame for selected file information
            data = {
                'Field': ['Author', 'Description', 'Source', 'Start Date', 'End Date'],
                'Value': [
                    selected_metadata['author'],
                    selected_metadata['description'],
                    selected_metadata['source'],
                    pd.to_datetime(selected_metadata['start_date']).strftime('%Y-%m-%d'),
                    pd.to_datetime(selected_metadata['end_date']).strftime('%Y-%m-%d')
                ]
            }
            df_info = pd.DataFrame(data)
            
        
            # Fetch file data from MongoDB
            file_data = list(collection.find({"file_id": selected_file_id}))
            
            if file_data:
                df_file_data = pd.DataFrame(file_data)
                
                # Add expander for filtering data
                with st.expander("Expand and see data for file", expanded=True):
                    show_columns = st.multiselect(
                        'Filter columns to display:', 
                        df_file_data.columns.tolist(), 
                        default=df_file_data.columns.tolist()
                    )
                    st.dataframe(df_file_data[show_columns], use_container_width=True)
                
                try:
                    # Provide download button for CSV
                    csv_data = df_file_data.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button("Download Data as CSV", csv_data, "data.csv", "text/csv")
                except OverflowError:
                    st.error("Error generating CSV file")
            else:
                st.write("No data found for the selected file.")
    else:
        st.write("No metadata found in the database.")

#******************************************************************************************

# ****************************************************************************************
# *****************************************************************************************
#This is the global part to be appear in all page
# Configuration de la page
st.set_page_config(page_title="Migration Data Hub", page_icon="🌍")



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






# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sidebar menu for navigation
def sidebar_menu():
    with st.sidebar:
        return option_menu(
            menu_title="Connexion",
            options=["View Data", "Welcome", "Login"],
            icons=["house", "person", "file-text"],
            default_index=0,
            orientation="vertical"
        )

# Function to display the welcome page
def display_welcome_page():
    # Load the background image
    image = Image.open("img5.jpg")

    # Title and slogan
    st.markdown("<h1 style='text-align: center; color: #004d99;'>Migration Data Hub</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #0066cc;'>Votre portail pour explorer, analyser et visualiser les données migratoires.</h2>", unsafe_allow_html=True)
    
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


    # Footer
    st.write("""
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: black;
            text-align: center;
            padding: 10px 0;
        }
        </style>
        <div class="footer">
            <p>Contact us: <a href="migraware:migraware@burkina.org">migraware@burkina.com</a></p>
            <p>&copy; 2024 MIGRAWARE</p>
        </div>
    """, unsafe_allow_html=True)



def log_user():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False


    if not st.session_state.logged_in:
        menu_option1 = sidebar_menu()

        if menu_option1 == "Welcome" and not st.session_state.logged_in:
           display_welcome_page()
        elif menu_option1 == "View Data":
            display_homepage()  # Ensure that this function is defined elsewhere
        elif menu_option1 == "Login":
            # log_user()  # Ensure that this function is defined elsewhere
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.success("Login successful")
                else:
                    st.error("Invalid credentials")
            if st.button("Create Account"):
                if username and password:
                    create_user(username, password)
                    st.success("Account created successfully")
                else:
                    st.error("Please fill in all fields")
    else:
            # Add the option_menu for navigation
            with st.sidebar:
                
                        # Handle other pages or fallback
                st.sidebar.image("data/logo4.png", caption="Human Migration")
                page = option_menu("Big Data", 
                    ["🏠 Home", "📁 Upload Data", "📂 View Data", "📝 Update Data", "📂 View Metadata", "🗑️ Delete a File", "🔍 Visualize Data", "🔍 Spatial Data", "🔍Prediction","🔍 Request on API", "🚪 Logout"],
                    icons=['house', 'upload', 'eye', 'pencil', 'file-earmark-text', 'trash', "bar-chart", "download", 'box-arrow-right'],
                    menu_icon="cast", default_index=0)

            if page == "🏠 Home":
                home3()
            # elif page == "📁 Upload Data":
            #     display_upload_data_page()
            # # Add more conditions for other pages if needed
            elif page == "📁 Upload Data":
                st.subheader("Upload a file")
                description = st.text_input("File Description")
                author = st.text_input("File Author")
                source = st.text_input("File Source")
                # data_type = st.text_input("Data Type")
                data_encapusule = st.selectbox("visibility", ["public", "private"])
                data_type = st.selectbox("Envergure", ["nationale", "internationale", "regionale"])
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
                uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])

                if uploaded_file and description and author and source and data_type:
                    if st.button("Upload Data"):
                        load_data_to_mongo(uploaded_file, uploaded_file.type.split('/')[1], description, author, source, data_type, start_date, end_date)

            elif page == "📂 View Data":
                st.subheader("View MongoDB Data")
                metadata = list(metadata_collection.find())
                if metadata:
                    df_metadata = pd.DataFrame(metadata)
                    st.dataframe(df_metadata)

                    selected_description = st.selectbox("Select a file description", df_metadata['description'])
                    if selected_description:
                        selected_metadata = df_metadata[df_metadata['description'] == selected_description].iloc[0]
                        selected_file_id = selected_metadata['_id']
                        
                        # Créer un DataFrame à partir des données
                        data = {
                            'Field': ['Author', 'Description', 'Source', 'Start Date', 'End Date'],
                            'Value': [
                                selected_metadata['author'],
                                selected_metadata['description'],
                                selected_metadata['source'],
                                selected_metadata['start_date'],
                                selected_metadata['end_date']
                            ]
                        }
                        df_info = pd.DataFrame(data)

                        # Afficher le tableau
                        # st.write("File Information:")
                        # st.dataframe(df_info)

                        st.write(f"Displaying data for file: {selected_file_id}")
                        
                        file_data = list(collection.find({"file_id": selected_file_id}))
                        if file_data:
                            df = pd.DataFrame(file_data)
                            st.dataframe(df)
                            # st.dataframe(edited_df)

                            try:
                                csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                                st.download_button("Download Data as CSV", csv_data, "data.csv", "text/csv")
                            except OverflowError:
                                st.error("Error generating CSV file")

                            num_data = df.select_dtypes(include='number')
                            if not num_data.empty:
                                st.subheader("Numeric Data Summary")
                                st.write(num_data.describe())
                            else:
                                st.write("No numeric data available for summary.")
                        else:
                            st.warning(f"No data found for file with file_id: {selected_file_id}")
                else:
                    st.warning("No files found in MongoDB")

            elif page == "📝 Update Data":
                st.subheader("Update Data")
                metadata = list(metadata_collection.find())
                if metadata:
                    df_metadata = pd.DataFrame(metadata)
                    descriptions_authors = df_metadata['description'] + " - " + df_metadata['author']
                    selected_description_author = st.selectbox("Select file description and author", descriptions_authors)

                    if selected_description_author:
                        selected_metadata = df_metadata[df_metadata['description'] + " - " + df_metadata['author'] == selected_description_author]
                        selected_file_id = selected_metadata.iloc[0]['_id']
                        
                        st.write(f"Selected file ID for update: {selected_file_id}")

                        uploaded_update_file = st.file_uploader("Choose a CSV file with specific columns for update", type=['csv'])
                        if uploaded_update_file is not None:
                            if st.button("Upload and Update Data"):
                                upload_by_update(uploaded_update_file)
                        

                        file_data = list(collection.find({"file_id": selected_file_id}))
                        if file_data:
                            df = pd.DataFrame(file_data)
                            st.write("Current Data:")
                        

                            # Afficher les données dans un tableau éditable
                            edited_df = st.data_editor(df, use_container_width=True)

                            # Ajouter un bouton pour sauvegarder les modifications
                            if st.button("Save Changes"):
                                updates = edited_df.to_dict(orient='records')
                                                        # Insertion des données dans MongoDB
                                

                                print("Données insérées avec succès dans MongoDB")
                                                        
                                for update in updates:
                                    if '_id' in update:

                                        del update['_id']  # Supprimer l'_id pour éviter les conflits
                                    collection.update_many({"file_id": selected_file_id}, {"$set": update})
                                

                                st.success("Données mises à jour avec succès dans MongoDB")
                            else:
                                st.warning(f"Aucune donnée trouvée pour le fichier avec file_id : {selected_file_id}")
                                # Ajouter un bouton pour télécharger les données en CSV
                                csv = df.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label="Télécharger les données en CSV",
                                    data=csv,
                                    file_name='data.csv',
                                    mime='text/csv',
                                )

                            # st.write("Updated Data Preview:")
                            # st.dataframe(edited_df)
                        else:
                            st.warning(f"No data found for file with file_id: {selected_file_id}")
                            
                else:
                    st.warning("No files found in MongoDB")

            elif page == "Delete Data":
                st.subheader("Delete Data")
                data = list(collection.find())
                if data:
                    df = pd.DataFrame(data)
                    selected_index = st.selectbox("Select the index of the row to delete", df.index)
                    selected_row = df.iloc[selected_index]

                    if st.button("Delete"):
                        if st.button("Confirm Deletion"):
                            delete_data_from_mongo(selected_row['_id'])
                        else:
                            st.warning("Please confirm the deletion.")

            elif page == "📂 View Metadata":
                st.subheader("View File Metadata")
                metadata = list(metadata_collection.find())
                if metadata:
                    df_metadata = pd.DataFrame(metadata)
                    # Create a column combining description and author
                    df_metadata['description_author'] = df_metadata['description'] + " - " + df_metadata['author']
                    
                    # Display the selectbox with combined description and author
                    selected_description_author = st.selectbox("Select file description and author", df_metadata['description_author'])
                    
                    # Find the selected description and author
                    selected_metadata = df_metadata[df_metadata['description_author'] == selected_description_author].iloc[0]
                    
                    # # Display the selected file metadata
                    # st.write("Selected File Metadata:")
                    # st.write(selected_metadata)

                    # Center the DataFrame display using Streamlit's columns
                    col1, col2, col3 = st.columns([1, 2, 1])

                    with col2:
                        # st.write("Selected File Metadata:")

                         # Create a download link for the metadata
                        csv = df_metadata.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download metadata as CSV",
                            data=csv,
                            file_name='metadata.csv',
                            mime='text/csv',
                            type='primary'
                        )

                        st.write(selected_metadata)

                        # Convert metadata to DataFrame
                        df_metadata = pd.DataFrame([selected_metadata])

                        # Display DataFrame
                        st.dataframe(df_metadata)

                         # Create a download link for the metadata with a red button
                        csv = df_metadata.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download metadata as CSV",
                            data=csv,
                            file_name='metadata.csv',
                            mime='text/csv',
                            key='download-csv',
                            help='Click to download the selected metadata',
                            on_click=None,
                            args=None,
                            kwargs=None,
                            disabled=False,
                            use_container_width=False,
                            type='primary'
                        )
                else:
                    st.warning("No metadata found in MongoDB")
                    

            elif page == "🗑️ Delete a File":
                st.subheader("Delete a File")
                metadata = list(metadata_collection.find())
                if metadata:
                    df_metadata = pd.DataFrame(metadata)
                    descriptions_authors = df_metadata['description'] + " - " + df_metadata['author']
                    selected_description_author = st.selectbox("Select file description and author", descriptions_authors)

                    if selected_description_author:
                        selected_metadata = df_metadata[df_metadata['description'] + " - " + df_metadata['author'] == selected_description_author]
                        selected_file_id = selected_metadata.iloc[0]['_id']
                        
                        if st.button("Delete File"):
                            if st.button("Confirm Deletion"):
                                delete_file(selected_file_id)
                            else:
                                st.warning("Please confirm the deletion.")
                else:
                    st.warning("No files found in MongoDB")
            elif page=="🔍 Visualize Data":
                        visualize()
            elif page =="🔍 Spatial Data":
                        main2()
            elif page =="🔍Prediction":
                        st.write("Upload your data to make it")
                        predict_migrant()
            elif page =="🔍 Request on API":
                    st.write("Choose the wanted request")
                    open_api_migrate()

            elif page == "🚪 Logout":
                st.session_state.logged_in = False
                st.success("Logged out successfully")
                
            else:
                display_homepage()

        
# Main application logic
def main():
    # Display the sidebar menuù
    log_user()


if __name__ == "__main__":
    main()