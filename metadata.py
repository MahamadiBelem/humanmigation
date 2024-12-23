import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import os


df = pd.read_csv()
df_selection = df.query(
    "Region == @region & Location == @location & Type == @construction"
)
# Home function
def Home():
    with st.expander("⏰ Les données sur les migrations"):
        showData = st.multiselect('Filter: ', df_selection.columns, default=[
            "Policy", "Expiry", "Location", "State", "Region", "Investment", "Type", "Destination", "Earthquake", "Flood", "Rating"])
        st.dataframe(df_selection[showData], use_container_width=True)
    
    # Compute top analytics
    total_investment = float(df_selection['Investment'].sum())
    investment_mode = float(df_selection['Investment'].mode().iloc[0])
    investment_mean = float(df_selection['Investment'].mean())
    investment_median = float(df_selection['Investment'].median())
    rating = float(df_selection['Rating'].sum())

    total1, total2, total3, total4, total5 = st.columns(5, gap='large')
    with total1:
        st.info('Investiment', icon="📌")
        st.metric(label="Total ", value=f"{total_investment:,.0f}")

    with total2:
        st.info('Minimal', icon="📌")
        st.metric(label="Minimal invest", value=f"{investment_mode:,.0f}")

    with total3:
        st.info('Moyenne', icon="📌")
        st.metric(label="Moyenne ", value=f"{investment_mean:,.0f}")

    with total4:
        st.info('Gains', icon="📌")
        st.metric(label="Médiane invest ", value=f"{investment_median:,.0f}")

    with total5:
        st.info('Taux', icon="📌")
        st.metric(label="Rating", value=numerize(rating), help=f""" Total Rating: {rating} """)

    st.markdown("""---""")
    st.markdown("""---""")
    st.markdown("""---""")