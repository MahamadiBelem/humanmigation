import streamlit as st
from streamlit_option_menu import option_menu
import warnings

# Suppress specific deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning, module="streamlit")

# Functions to display different pages
def dashboard_page():
    st.title("Dashboard Page")
    st.write("Welcome to the Dashboard!")

def reports_page():
    st.title("Reports Page")
    st.write("Here are your reports.")

def analytics_page():
    st.title("Analytics Page")
    st.write("Analytics section.")

def profile_page():
    st.title("Profile Page")
    st.write("Edit your profile here.")

def preferences_page():
    st.title("Preferences Page")
    st.write("Set your preferences here.")

def security_page():
    st.title("Security Page")
    st.write("Manage your security settings here.")

def upload_data_page():
    st.title("Upload Data Page")
    st.write("Upload your data here.")

def update_data_page():
    st.title("Update Data Page")
    st.write("Update your data here.")

def delete_data_page():
    st.title("Delete Data Page")
    st.write("Delete your data here.")

def view_data_page():
    st.title("View Data Page")
    st.write("View your data here.")

# Main menu
with st.sidebar:
    main_menu = option_menu(
        "Main Menu", 
        ["Migration Data", "Migration Factors", "Geo-spatiale Data"],
        icons=["database", "chart-line", "globe"],
        menu_icon="cast",
        default_index=0
    )

# Sub-menus based on the main menu selection
if main_menu == "Migration Data":
    st.subheader("Migration Data Menu")
    sub_menu = st.selectbox("Choose an option", ["Upload Data", "Update Data", "Delete Data", "View Data"])
    if sub_menu == "Upload Data":
        st.experimental_set_query_params(page="upload_data")
    elif sub_menu == "Update Data":
        st.experimental_set_query_params(page="update_data")
    elif sub_menu == "Delete Data":
        st.experimental_set_query_params(page="delete_data")
    elif sub_menu == "View Data":
        st.experimental_set_query_params(page="view_data")

elif main_menu == "Migration Factors":
    st.subheader("Migration Factors Menu")
    sub_menu = st.selectbox("Choose an option", ["Upload Data", "Update Data", "Delete Data", "View Data"])
    if sub_menu == "Upload Data":
        st.experimental_set_query_params(page="upload_data")
    elif sub_menu == "Update Data":
        st.experimental_set_query_params(page="update_data")
    elif sub_menu == "Delete Data":
        st.experimental_set_query_params(page="delete_data")
    elif sub_menu == "View Data":
        st.experimental_set_query_params(page="view_data")

elif main_menu == "Geo-spatiale Data":
    st.subheader("Geo-spatiale Data Menu")
    sub_menu = st.selectbox("Choose an option", ["Upload Data", "Update Data", "Delete Data", "View Data"])
    if sub_menu == "Upload Data":
        st.experimental_set_query_params(page="upload_data")
    elif sub_menu == "Update Data":
        st.experimental_set_query_params(page="update_data")
    elif sub_menu == "Delete Data":
        st.experimental_set_query_params(page="delete_data")
    elif sub_menu == "View Data":
        st.experimental_set_query_params(page="view_data")

# Check query parameters to display the correct page
query_params = st.experimental_get_query_params()
if query_params.get("page") == ["upload_data"]:
    upload_data_page()
elif query_params.get("page") == ["update_data"]:
    update_data_page()
elif query_params.get("page") == ["delete_data"]:
    delete_data_page()
elif query_params.get("page") == ["view_data"]:
    view_data_page()
elif query_params.get("page") == ["dashboard"]:
    dashboard_page()
elif query_params.get("page") == ["reports"]:
    reports_page()
elif query_params.get("page") == ["analytics"]:
    analytics_page()
elif query_params.get("page") == ["profile"]:
    profile_page()
elif query_params.get("page") == ["preferences"]:
    preferences_page()
elif query_params.get("page") == ["security"]:
    security_page()




# import streamlit as st
# from streamlit_option_menu import option_menu

# # Functions to display different pages
# def dashboard_page():
#     st.title("Dashboard Page")
#     st.write("Welcome to the Dashboard!")

# def reports_page():
#     st.title("Reports Page")
#     st.write("Here are your reports.")

# def analytics_page():
#     st.title("Analytics Page")
#     st.write("Analytics section.")

# def profile_page():
#     st.title("Profile Page")
#     st.write("Edit your profile here.")

# def preferences_page():
#     st.title("Preferences Page")
#     st.write("Set your preferences here.")

# def security_page():
#     st.title("Security Page")
#     st.write("Manage your security Migration Factors here.")

# # Main menu
# with st.sidebar:
#     main_menu = option_menu("Main Menu", ["Migration Data", "Migration Factors", "Geo-spatiale Data"])

# # Sub-menus based on the main menu selection
# if main_menu == "Migration Data":
#     st.subheader("Migration Data Menu")
#     sub_menu = st.selectbox("Choose an option", ["Dashboard", "Reports", "Analytics"])
#     if sub_menu == "Dashboard":
#         st.experimental_set_query_params(page="dashboard")
#     elif sub_menu == "Reports":
#         st.experimental_set_query_params(page="reports")
#     elif sub_menu == "Analytics":
#         st.experimental_set_query_params(page="analytics")

# elif main_menu == "Migration Factors":
#     st.subheader("Migration Factors Menu")
#     sub_menu = st.radio("Choose an option", ["Profile", "Preferences", "Security"])
#     if sub_menu == "Profile":
#         st.experimental_set_query_params(page="profile")
#     elif sub_menu == "Preferences":
#         st.experimental_set_query_params(page="preferences")
#     elif sub_menu == "Security":
#         st.experimental_set_query_params(page="security")

# elif main_menu == "Geo-spatiale Data":
#     st.write("This is the Geo-spatiale Data section.")

# # Check query parameters to display the correct page
# query_params = st.experimental_get_query_params()
# if query_params.get("page") == ["dashboard"]:
#     dashboard_page()
# elif query_params.get("page") == ["reports"]:
#     reports_page()
# elif query_params.get("page") == ["analytics"]:
#     analytics_page()
# elif query_params.get("page") == ["profile"]:
#     profile_page()
# elif query_params.get("page") == ["preferences"]:
#     preferences_page()
# elif query_params.get("page") == ["security"]:
#     security_page()


# import streamlit as st
# from streamlit_option_menu import option_menu

# # Main menu
# with st.sidebar:
#     main_menu = option_menu("Main Menu", ["Migration Data", "Migration Factors", "Geo-spatiale Data"])

# # Sub-menus based on the main menu selection
# if main_menu == "Migration Data":
#     st.subheader("Migration Data Menu")
#     sub_menu = st.selectbox("Choose an option", ["Dashboard", "Reports", "Analytics"])
#     if sub_menu == "Dashboard":
#         st.write("Welcome to the Dashboard!")
#     elif sub_menu == "Reports":
#         st.write("Here are your reports.")
#     elif sub_menu == "Analytics":
#         st.write("Analytics section.")

# elif main_menu == "Migration Factors":
#     st.subheader("Migration Factors Menu")
#     sub_menu = st.radio("Choose an option", ["Profile", "Preferences", "Security"])
#     if sub_menu == "Profile":
#         st.write("Edit your profile here.")
#     elif sub_menu == "Preferences":
#         st.write("Set your preferences here.")
#     elif sub_menu == "Security":
#         st.write("Manage your security Migration Factors here.")

# elif main_menu == "Geo-spatiale Data":
#     st.write("This is the Geo-spatiale Data section.")

# import streamlit as st
# from streamlit_option_menu import option_menu

# # Main menu in the sidebar
# with st.sidebar:
#     main_menu = option_menu("Main Menu", ["Migration Data", "Migration Factors", "Geo-spatiale Data"])

#     # Sub-menu under Migration Data
#     if main_menu == "Migration Data":
#         st.subheader("Migration Data Menu")
#         sub_menu = st.selectbox("Choose an option", ["Dashboard", "Reports", "Analytics"])
#         if sub_menu == "Dashboard":
#             st.write("Welcome to the Dashboard!")
#         elif sub_menu == "Reports":
#             st.write("Here are your reports.")
#         elif sub_menu == "Analytics":
#             st.write("Analytics section.")

#     elif main_menu == "Migration Factors":
#         st.subheader("Migration Factors Menu")
#         st.write("Choose an option from the Migration Factors menu.")

#     elif main_menu == "Geo-spatiale Data":
#         st.write("This is the Geo-spatiale Data section.")

