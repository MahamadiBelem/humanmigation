import streamlit as st
from streamlit_keycloak import login

# Connexion avec Keycloak via streamlit_keycloak
keycloak = login(
    url="http://localhost:8080",  # URL du serveur Keycloak
    realm="humanmigration",      # Nom de votre realm
    client_id="humanmigration"   # Client ID de votre application Keycloak
)

# Vérifiez l'état de la session après la connexion
if "keycloak_token" in st.session_state:
    st.session_state["authenticated"] = True
    token = st.session_state["keycloak_token"]  # Récupère le token d'accès
    username = st.session_state.get("keycloak_username", "Utilisateur")  # Récupère le nom d'utilisateur

    st.write(f"Bienvenue, {username}. Vous êtes connecté.")
    
    if st.button("Se déconnecter"):
        # Réinitialisation de la session pour simuler la déconnexion
        st.session_state["authenticated"] = False
        st.session_state.pop("keycloak_token", None)  # Efface le token de session
        st.session_state.pop("keycloak_username", None)  # Efface le nom d'utilisateur
        st.write("Vous avez été déconnecté.")
else:
    st.write("Veuillez vous connecter pour accéder à l'application.")

# Débogage : Affichage complet de la session
st.write("Contenu de la session:", st.session_state)  # Affiche ce qui est dans la session

# Optionnel: Forcer un rafraîchissement après l'authentification pour bien appliquer les modifications
if "keycloak_token" in st.session_state and st.session_state["authenticated"]:
    st.experimental_rerun()
