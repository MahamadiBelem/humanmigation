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
from archive.visualisation import visualize
from api_ui import open_api_migrate
from bson import ObjectId

# This home is the home after login succesfullly
def home_admin():
    # Chargement de l'image de fond
    image = Image.open("assets/img/img7.jpg")

    # Titre et slogan
    # st.markdown("<h1 style='text-align: center; color: #004d99;'>Migration Data Hub</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #0066cc;'>Your portal to explore, analyze and visualize migration data.</h2>", unsafe_allow_html=True)

    # # Menu de navigation
    # menu = st.sidebar.selectbox("Autres", ["À propos", "Contact"])

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

    # # Témoignages et avis
    # st.markdown("""
    #     <h3>Témoignages et Avis</h3>
    #     <p><strong>Témoignages d’Utilisateurs :</strong> Découvrez ce que nos utilisateurs disent de nous.</p>
    #     <p><strong>Évaluations :</strong> Note moyenne : 4.8/5</p>
    #     """, unsafe_allow_html=True)

    # # Mises à jour et actualités
    # st.markdown("""
    #     <h3>Mises à Jour et Actualités</h3>
    #     <p><strong>Dernières Nouvelles :</strong> Restez informé des dernières mises à jour et actualités sur les migrations.</p>
    #     """, unsafe_allow_html=True)

    # # Style additionnel
    # st.markdown("""
    #     <style>
    #     body {font-family: Arial, sans-serif;}
    #     h1 {font-size: 2.5em; color: #004d99;}
    #     h2 {font-size: 1.5em; color: #0066cc;}
    #     h3 {font-size: 1.2em; color: #003366;}
    #     </style>
    #     """, unsafe_allow_html=True)
#*****************************************************************************************
#*****************************************************************************************