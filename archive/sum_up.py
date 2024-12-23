import streamlit as st
from streamlit.components.v1 import html

def display_migration_summary():
    # Custom CSS
    custom_css = """
    <style>
        .custom-container {
            background-color: #f5f5f5;
            font-family: 'Arial', sans-serif;
            font-size: 16px;
        }
        .custom-container .stApp {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .custom-container h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        .custom-container h2 {
            color: #34495e;
            font-size: 2em;
            margin-top: 30px;
            margin-bottom: 10px;
        }
        .custom-container p, .custom-container li {
            color: #7f8c8d;
            font-size: 16px;  /* Taille de la police des puces */
            line-height: 1.6;
        }
        .custom-container ul {
            padding-left: 20px;
        }
        .custom-container ul li {
            margin-bottom: 10px;
        }
    </style>
    """
    html(custom_css, height=0)

    st.markdown('<div class="custom-container">', unsafe_allow_html=True)

    # st.title("Big Data Platform for Migration Policy")

    st.header("Overview")
    st.write("Dealing with population migration is a significant challenge for policymakers, especially in developing countries. The lack of relevant data and tools hinders effective migration policy formulation and implementation.")

    st.header("Challenges")
    st.write("""
    1. <span style="color: #e74c3c;">**Data Fragmentation**</span>: Researchers collect data in various formats and for different purposes, leading to fragmented information.
    2. <span style="color: #e74c3c;">**Lack of Analytical Tools**</span>: Despite the large volumes of data, there are no tools to analyze and provide decision-making indicators, recommendations, and predictions.
    3. <span style="color: #e74c3c;">**Redundancy and Waste**</span>: Data is often collected multiple times, wasting time and resources without adding value.
    4. <span style="color: #e74c3c;">**Diverse Expert Opinions**</span>: Experts have differing views on migration issues, which need to be integrated for a comprehensive understanding.
    """, unsafe_allow_html=True)

    st.header("Current Solutions")
    st.write("<span style='color: #e74c3c;'>**Ontology-Based Databases**</span>: Tools like the ontologically-based database on migration in West Africa link data but lack analytical and visualization capabilities.", unsafe_allow_html=True)

    st.header("Proposed Big Data Solution")
    st.write("""
    - <span style="color: #e74c3c;">**Integration Framework**</span>: Develop a big data platform using Hadoop to integrate and visualize migration data.
    - <span style="color: #e74c3c;">**Data Sources**</span>: Include data on climate, demography, geography, scientific evolution, soils, households, socio-economic activities, and administrative organization.
    - <span style="color: #e74c3c;">**Technologies**</span>: Combine several migration databases and ontology databases.
    - <span style="color: #e74c3c;">**Processing**</span>: Utilize MapReduce paradigm for processing and visualization tools to display indicators and migration trends.
    """, unsafe_allow_html=True)

    st.header("Goals")
    st.write("""
    - <span style="color: #e74c3c;">**Comprehensive Data Integration**</span>: Create a unified framework for acquiring and integrating migration data.
    - <span style="color: #e74c3c;">**Enhanced Decision-Making**</span>: Provide tools for analyzing data and visualizing relevant decision indicators and recommendations.
    - <span style="color: #e74c3c;">**Efficient Resource Use**</span>: Reduce redundancy and improve the value of collected data.
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
     display_migration_summary()
