import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
def visualize():
    # Improved dataset for human migration with West African countries
    data = {
        'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
        'Country': ['Nigeria', 'Ghana', 'Senegal', 'Ivory Coast', 'Burkina Faso', 'Mali', 'Niger', 'Guinea', 'Togo'],
        'Migrants': [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000],
        'Emigrants': [500, 700, 800, 1200, 1500, 1800, 2000, 2200, 2500]
    }

    df = pd.DataFrame(data)

    # Title
    st.title('Human Migration Data Visualization')

    # Sidebar for selecting visualization type
    st.sidebar.title('Select Visualization Type')
   # Sidebar menu for selecting chart type
    with st.sidebar:
        visualization_type = option_menu(
            'Choose a chart type:',
            ['Bar Chart', 'Line Chart', 'Area Chart', 'Scatter Plot', 'Histogram', 'Pie Chart', 'Box Plot', 'Heatmap'],
            icons=['bar-chart', 'line-chart', 'area-chart', 'scatter-plot', 'histogram', 'pie-chart', 'box-plot', 'heatmap'],
            menu_icon="cast",
            default_index=0,
        )

    # Display the selected chart type
    st.write(f'You selected: {visualization_type}')

    # Bar Chart
    if visualization_type == 'Bar Chart':
        st.bar_chart(df.set_index('Year')[['Migrants', 'Emigrants']])

    # Line Chart
    elif visualization_type == 'Line Chart':
        st.line_chart(df.set_index('Year')[['Migrants', 'Emigrants']])

    # Area Chart
    elif visualization_type == 'Area Chart':
        st.area_chart(df.set_index('Year')[['Migrants', 'Emigrants']])

    # Scatter Plot
    elif visualization_type == 'Scatter Plot':
        st.write('Scatter Plot')
        fig, ax = plt.subplots()
        ax.scatter(df['Year'], df['Migrants'], label='Migrants')
        ax.scatter(df['Year'], df['Emigrants'], label='Emigrants')
        ax.legend()
        st.pyplot(fig)

    # Histogram
    elif visualization_type == 'Histogram':
        st.write('Histogram')
        fig, ax = plt.subplots()
        ax.hist(df['Migrants'], bins=10, alpha=0.5, label='Migrants')
        ax.hist(df['Emigrants'], bins=10, alpha=0.5, label='Emigrants')
        ax.legend()
        st.pyplot(fig)

    # Pie Chart
    elif visualization_type == 'Pie Chart':
        st.write('Pie Chart')
        fig, ax = plt.subplots()
        ax.pie(df['Migrants'], labels=df['Country'], autopct='%1.1f%%')
        st.pyplot(fig)

    # Box Plot
    elif visualization_type == 'Box Plot':
        st.write('Box Plot')
        fig, ax = plt.subplots()
        sns.boxplot(data=df[['Migrants', 'Emigrants']], ax=ax)
        st.pyplot(fig)

    # Heatmap
    elif visualization_type == 'Heatmap':
        st.write('Heatmap')
        fig, ax = plt.subplots()
        sns.heatmap(df[['Migrants', 'Emigrants']].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # Display the dataframe
    st.write('Human Migration Data')
    st.write(df)

def test_uplolad():
    # Function to load data
    def load_data(file):
        df = pd.read_csv(file)
        return df

    # Title
    st.title('Human Migration Data Visualization')

    # Sidebar for selecting visualization type
    st.sidebar.title('Select Visualization Type')
    visualization_type = st.sidebar.selectbox(
        'Choose a chart type:', 
        ['Bar Chart', 'Line Chart', 'Area Chart', 'Scatter Plot', 'Histogram', 'Pie Chart', 'Box Plot', 'Heatmap']
    )

    # File uploader
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

    # Load data
    if uploaded_file is not None:
        df = load_data(uploaded_file)
    else:
        # Default dataset for human migration with West African countries
        data = {
            'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
            'Country': ['Nigeria', 'Ghana', 'Senegal', 'Ivory Coast', 'Burkina Faso', 'Mali', 'Niger', 'Guinea', 'Togo'],
            'Migrants': [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000],
            'Emigrants': [500, 700, 800, 1200, 1500, 1800, 2000, 2200, 2500]
        }
        df = pd.DataFrame(data)

    # Bar Chart
    if visualization_type == 'Bar Chart':
        st.bar_chart(df.set_index('Year')[['Migrants', 'Emigrants']])

    # Line Chart
    elif visualization_type == 'Line Chart':
        st.line_chart(df.set_index('Year')[['Migrants', 'Emigrants']])

    # Area Chart
    elif visualization_type == 'Area Chart':
        st.area_chart(df.set_index('Year')[['Migrants', 'Emigrants']])

    # Scatter Plot
    elif visualization_type == 'Scatter Plot':
        st.write('Scatter Plot')
        fig, ax = plt.subplots()
        ax.scatter(df['Year'], df['Migrants'], label='Migrants')
        ax.scatter(df['Year'], df['Emigrants'], label='Emigrants')
        ax.legend()
        st.pyplot(fig)

    # Histogram
    elif visualization_type == 'Histogram':
        st.write('Histogram')
        fig, ax = plt.subplots()
        ax.hist(df['Migrants'], bins=10, alpha=0.5, label='Migrants')
        ax.hist(df['Emigrants'], bins=10, alpha=0.5, label='Emigrants')
        ax.legend()
        st.pyplot(fig)

    # Pie Chart
    elif visualization_type == 'Pie Chart':
        st.write('Pie Chart')
        fig, ax = plt.subplots()
        ax.pie(df['Migrants'], labels=df['Country'], autopct='%1.1f%%')
        st.pyplot(fig)

    # Box Plot
    elif visualization_type == 'Box Plot':
        st.write('Box Plot')
        fig, ax = plt.subplots()
        sns.boxplot(data=df[['Migrants', 'Emigrants']], ax=ax)
        st.pyplot(fig)

    # Heatmap
    elif visualization_type == 'Heatmap':
        st.write('Heatmap')
        fig, ax = plt.subplots()
        sns.heatmap(df[['Migrants', 'Emigrants']].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # Display the dataframe
    st.write('Human Migration Data')
    st.write(df)


