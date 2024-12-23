import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import streamlit as st
import folium
from statsmodels.tsa.arima.model import ARIMA
from streamlit_folium import folium_static

def forecast_migrants(migrants_series):
    model = ARIMA(migrants_series, order=(1, 1, 1))  # Adjust order based on your data
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=5)  # Forecast for the next 5 years
    return forecast

def main():
    # Enhanced dataset with demographic data for selected cities across different continents
    data = {
        'Neighborhood': ['Nairobi', 'Lagos', 'Accra', 'Cairo', 'Johannesburg', 
                        'Addis Ababa', 'Dar es Salaam', 'Kinshasa', 'Cape Town', 'Abidjan',
                        'London', 'Berlin', 'Paris', 'Madrid', 'Rome',
                        'New York', 'Los Angeles', 'Toronto', 'Sao Paulo', 'Mexico City',
                        'Sydney', 'Auckland', 'Wellington', 'Brisbane', 'Melbourne',
                        'Tokyo', 'Beijing', 'Mumbai', 'Seoul', 'Bangkok'],
        'GDP Growth Rate (%)': [5.5, 3.1, 5.2, 4.0, 3.6, 
                                6.1, 7.0, 4.5, 3.9, 5.0,
                                2.5, 1.9, 1.7, 2.2, 1.5,
                                3.0, 4.0, 3.5, 2.8, 3.4,
                                2.9, 3.1, 3.2, 3.0, 2.8,
                                1.8, 5.0, 5.4, 2.1, 3.0],
        'Unemployment Rate (%)': [6.5, 15.0, 6.8, 10.0, 25.0, 
                                  15.5, 10.2, 12.0, 18.0, 9.5,
                                  5.0, 4.5, 8.0, 14.0, 9.0,
                                  7.5, 9.0, 6.0, 11.0, 4.8,
                                  4.0, 4.5, 5.2, 4.0, 3.8,
                                  3.0, 4.0, 7.0, 3.5, 5.0],
        'Living Conditions Index': [60, 55, 70, 50, 40, 
                                    65, 60, 50, 75, 65,
                                    80, 75, 85, 80, 78,
                                    70, 65, 75, 60, 55,
                                    85, 90, 88, 86, 89,
                                    70, 72, 65, 67, 68],
        'Population Density (people/km²)': [4200, 3200, 1300, 1900, 1600, 
                                             1800, 2500, 1500, 1200, 2500,
                                             5500, 4000, 2100, 3200, 1600,
                                             11000, 8500, 6000, 8500, 5000,
                                             4000, 1800, 3000, 2000, 4200,
                                             6100, 1300, 2000, 8000, 2000],
        'Median Age (years)': [24, 18, 26, 24, 30, 
                               20, 19, 22, 27, 28,
                               40, 43, 41, 38, 35,
                               36, 34, 40, 31, 30,
                               34, 37, 36, 35, 33,
                               48, 36, 29, 41, 30],
        'Number of Migrants': [5000, 3000, 6000, 2000, 4000, 
                               3500, 5500, 6500, 7000, 2500,
                               8000, 10000, 9500, 11000, 9000,
                               12000, 11000, 9000, 15000, 13000,
                               5000, 6000, 7000, 8000, 7500,
                               3000, 4500, 5000, 6000, 4000],
        'Latitude': [-1.286389, 6.524, 5.6037, 30.0444, -26.2041, 
                     9.03, -6.7924, -4.441, -33.918861, 5.345,
                     51.5074, 52.5200, 48.8566, 40.4168, 41.9028,
                     40.7128, 34.0522, 43.65107, -23.5505, 19.4326,
                     -33.8688, -36.8485, -41.2865, -27.4705, -37.8136,
                     35.6762, 39.9042, 19.0760, 37.5665, 13.7563],
        'Longitude': [36.817223, 3.3792, -0.1870, 31.2357, 28.0473, 
                      38.7469, 39.2083, 15.2663, 18.4233, -4.008,
                      -0.1278, 13.4050, 2.3522, -3.7038, 12.4964,
                      -74.0060, -118.2437, -79.3832, -46.6333, -99.1332,
                      151.2093, 174.7633, 175.0154, 153.0211, 144.9632,
                      139.6503, 116.4074, 72.8777, 126.9780, 100.5167]
    }

    df = pd.DataFrame(data)

    # User input for parameters
    st.title('Population Change Prediction Due to Migration and Demographic Analysis')

    # Forecasting Migrants
    migrants_forecast = forecast_migrants(df['Number of Migrants'])
    df_forecast = pd.DataFrame({
        'Year': np.arange(2025, 2030),
        'Predicted Migrants': migrants_forecast
    })

    # Menu for visualization type
    menu_option = st.selectbox("Choose Visualization Type", ["Map", "Histogram", "Data Table", "Line Chart", "Bar Chart"])

    if menu_option == "Map":
        # Visualization: Choropleth Map
        m = folium.Map(location=[0, 20], zoom_start=2)  # Center on Africa
        for index, row in df.iterrows():
            folium.CircleMarker(
                location=(row['Latitude'], row['Longitude']),
                radius=row['Number of Migrants'] / 1000,  # Scale for visibility
                color='blue',
                fill=True,
                fill_opacity=0.6,
                popup=f"{row['Neighborhood']}: {row['Number of Migrants']} Migrants"
            ).add_to(m)

        st.write("### Predicted Migrants Map")
        folium_static(m)

    elif menu_option == "Histogram":
        # Histogram of predicted migrants
        st.write("### Histogram of Predicted Migrants (2025-2030)")
        plt.figure(figsize=(10, 6))
        plt.hist(df_forecast['Predicted Migrants'], bins=10, color='blue', alpha=0.7)
        plt.title('Distribution of Predicted Number of Migrants (2025-2030)')
        plt.xlabel('Predicted Number of Migrants')
        plt.ylabel('Frequency')
        st.pyplot(plt)

    elif menu_option == "Data Table":
        # Display predictions in a data table
        st.write("### Predicted Migrants by Neighborhood and Year")
        st.write(df_forecast)

    elif menu_option == "Line Chart":
        # Line chart of predicted migrants over the years
        st.write("### Line Chart of Predicted Migrants (2025-2030)")
        plt.figure(figsize=(10, 6))
        plt.plot(df_forecast['Year'], df_forecast['Predicted Migrants'], marker='o', color='blue')
        plt.title('Predicted Number of Migrants Over the Next 5 Years')
        plt.xlabel('Year')
        plt.ylabel('Predicted Number of Migrants')
        plt.xticks(df_forecast['Year'])
        st.pyplot(plt)

    elif menu_option == "Bar Chart":
        # Bar chart comparing predicted migrants across neighborhoods
        st.write("### Bar Chart of Predicted Migrants by Neighborhood")
        plt.figure(figsize=(10, 6))
        plt.bar(df['Neighborhood'], df['Number of Migrants'], color='blue', alpha=0.7)
        plt.title('Predicted Number of Migrants by Neighborhood')
        plt.xlabel('Neighborhood')
        plt.ylabel('Number of Migrants')
        plt.xticks(rotation=45)
        st.pyplot(plt)

    # Model evaluation
    X = df[['GDP Growth Rate (%)', 'Unemployment Rate (%)', 'Living Conditions Index', 
             'Population Density (people/km²)', 'Median Age (years)']]
    y_migrants = df['Number of Migrants']

    X_train, X_test, y_train_migrants, y_test_migrants = train_test_split(
        X, y_migrants, test_size=0.2, random_state=0
    )

    pipeline_migrants = make_pipeline(
        StandardScaler(),
        LinearRegression()
    )
    pipeline_migrants.fit(X_train, y_train_migrants)

    # Predictions
    df['Predicted Migrants'] = pipeline_migrants.predict(X)

    # Evaluate model
    y_pred_migrants = pipeline_migrants.predict(X_test)
    mse_migrants = mean_squared_error(y_test_migrants, y_pred_migrants)

    st.write("### Model Evaluation")
    st.write(f"Mean Squared Error for Number of Migrants: {mse_migrants:.2f}")

if __name__ == "__main__":
    main()





# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import mean_squared_error
# import streamlit as st
# import folium
# from statsmodels.tsa.arima.model import ARIMA
# from streamlit_folium import folium_static

# def forecast_migrants(migrants_series):
#     model = ARIMA(migrants_series, order=(1, 1, 1))  # Adjust order based on your data
#     model_fit = model.fit()
#     forecast = model_fit.forecast(steps=5)  # Forecast for the next 5 years
#     return forecast

# def main():
#     # Enhanced dataset with demographic data for selected African cities
#     data = {
#         'Neighborhood': ['Nairobi', 'Lagos', 'Accra', 'Cairo', 'Johannesburg', 
#                         'Addis Ababa', 'Dar es Salaam', 'Kinshasa', 'Cape Town', 'Abidjan'],
#         'GDP Growth Rate (%)': [5.5, 3.1, 5.2, 4.0, 3.6, 
#                                 6.1, 7.0, 4.5, 3.9, 5.0],
#         'Unemployment Rate (%)': [6.5, 15.0, 6.8, 10.0, 25.0, 
#                                   15.5, 10.2, 12.0, 18.0, 9.5],
#         'Living Conditions Index': [60, 55, 70, 50, 40, 
#                                     65, 60, 50, 75, 65],
#         'Population Density (people/km²)': [4200, 3200, 1300, 1900, 1600, 
#                                              1800, 2500, 1500, 1200, 2500],
#         'Median Age (years)': [24, 18, 26, 24, 30, 
#                                20, 19, 22, 27, 28],
#         'Number of Migrants': [5000, 3000, 6000, 2000, 4000, 
#                                3500, 5500, 6500, 7000, 2500],
#         'Latitude': [-1.286389, 6.524, 5.6037, 30.0444, -26.2041, 
#                      9.03, -6.7924, -4.441, -33.918861, 5.345],
#         'Longitude': [36.817223, 3.3792, -0.1870, 31.2357, 28.0473, 
#                       38.7469, 39.2083, 15.2663, 18.4233, -4.008]
#     }

#     df = pd.DataFrame(data)

#     # User input for parameters
#     st.title('Population Change Prediction Due to Migration and Demographic Analysis')

#     # Forecasting Migrants
#     migrants_forecast = forecast_migrants(df['Number of Migrants'])
#     df_forecast = pd.DataFrame({
#         'Year': np.arange(2025, 2030),
#         'Predicted Migrants': migrants_forecast
#     })

#     # Menu for visualization type
#     menu_option = st.selectbox("Choose Visualization Type", ["Map", "Histogram", "Data Table", "Line Chart", "Bar Chart"])

#     if menu_option == "Map":
#         # Visualization: Choropleth Map
#         m = folium.Map(location=[0, 20], zoom_start=2)  # Center on Africa
#         for index, row in df.iterrows():
#             folium.CircleMarker(
#                 location=(row['Latitude'], row['Longitude']),
#                 radius=row['Number of Migrants'] / 1000,  # Scale for visibility
#                 color='blue',
#                 fill=True,
#                 fill_opacity=0.6,
#                 popup=f"{row['Neighborhood']}: {row['Number of Migrants']} Migrants"
#             ).add_to(m)

#         st.write("### Predicted Migrants Map")
#         folium_static(m)

#     elif menu_option == "Histogram":
#         # Histogram of predicted migrants
#         st.write("### Histogram of Predicted Migrants (2025-2030)")
#         plt.figure(figsize=(10, 6))
#         plt.hist(df_forecast['Predicted Migrants'], bins=10, color='blue', alpha=0.7)
#         plt.title('Distribution of Predicted Number of Migrants (2025-2030)')
#         plt.xlabel('Predicted Number of Migrants')
#         plt.ylabel('Frequency')
#         st.pyplot(plt)

#     elif menu_option == "Data Table":
#         # Display predictions in a data table
#         st.write("### Predicted Migrants by Neighborhood and Year")
#         st.write(df_forecast)

#     elif menu_option == "Line Chart":
#         # Line chart of predicted migrants over the years
#         st.write("### Line Chart of Predicted Migrants (2025-2030)")
#         plt.figure(figsize=(10, 6))
#         plt.plot(df_forecast['Year'], df_forecast['Predicted Migrants'], marker='o', color='blue')
#         plt.title('Predicted Number of Migrants Over the Next 5 Years')
#         plt.xlabel('Year')
#         plt.ylabel('Predicted Number of Migrants')
#         plt.xticks(df_forecast['Year'])
#         st.pyplot(plt)

#     elif menu_option == "Bar Chart":
#         # Bar chart comparing predicted migrants across neighborhoods
#         st.write("### Bar Chart of Predicted Migrants by Neighborhood")
#         plt.figure(figsize=(10, 6))
#         plt.bar(df['Neighborhood'], df['Number of Migrants'], color='blue', alpha=0.7)
#         plt.title('Predicted Number of Migrants by Neighborhood')
#         plt.xlabel('Neighborhood')
#         plt.ylabel('Number of Migrants')
#         plt.xticks(rotation=45)
#         st.pyplot(plt)

#     # Model evaluation
#     X = df[['GDP Growth Rate (%)', 'Unemployment Rate (%)', 'Living Conditions Index', 
#              'Population Density (people/km²)', 'Median Age (years)']]
#     y_migrants = df['Number of Migrants']

#     X_train, X_test, y_train_migrants, y_test_migrants = train_test_split(
#         X, y_migrants, test_size=0.2, random_state=0
#     )

#     pipeline_migrants = make_pipeline(
#         StandardScaler(),
#         LinearRegression()
#     )
#     pipeline_migrants.fit(X_train, y_train_migrants)

#     # Predictions
#     df['Predicted Migrants'] = pipeline_migrants.predict(X)

#     # Evaluate model
#     y_pred_migrants = pipeline_migrants.predict(X_test)
#     mse_migrants = mean_squared_error(y_test_migrants, y_pred_migrants)

#     st.write("### Model Evaluation")
#     st.write(f"Mean Squared Error for Number of Migrants: {mse_migrants:.2f}")

# if __name__ == "__main__":
#     main()
