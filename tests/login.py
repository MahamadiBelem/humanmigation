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

# ****************************************************************************************
# *****************************************************************************************

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['migration_in_world']
collection = db['mycollection']
metadata_collection = db['metadata']
users_collection = db['users']


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

# create a user and login by providing the require field
def create_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({"username": username, "password": hashed})

def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return True
    return False


# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sidebar menu for navigation
def sidebar_menu():
    with st.sidebar:
        return option_menu(
            menu_title="Connexion",
            options=["Welcome", "Login"],
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




def log_user():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False


    if not st.session_state.logged_in:
        menu_option1 = sidebar_menu()

        if menu_option1 == "Welcome" and not st.session_state.logged_in:
           display_welcome_page()
        # elif menu_option1 == "View Data":
        #     display_welcome_page()  # Ensure that this function is defined elsewhere
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
                display_welcome_page()
            # elif page == "📁 Upload Data":
            #     display_upload_data_page()
            # # Add more conditions for other pages if needed

