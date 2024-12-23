import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import streamlit as st
import folium
from folium.plugins import HeatMap

# Extended dataset including neighborhood-level data
data = {
    'Neighborhood': ['Downtown', 'Uptown', 'Suburb', 'Countryside', 'Historic District', 
                      'Central', 'Old Town', 'New Town', 'Industrial Zone', 'Riverside'],
    'GDP Growth Rate (%)': [3.5, 2.1, 4.0, 1.5, 3.0, 2.8, 3.2, 3.9, 4.5, 2.0],
    'Unemployment Rate (%)': [5.0, 6.5, 4.2, 7.0, 5.8, 6.0, 5.5, 4.9, 3.8, 6.2],
    'Living Conditions Index': [70, 60, 80, 50, 65, 55, 75, 85, 90, 60],
    'Number of Migrants': [5000, 3000, 6000, 2000, 4000, 3500, 5500, 6500, 7000, 2500],
    'Latitude': [40.7128, 40.7831, 40.7128, 40.7306, 40.7580, 40.7306, 40.7411, 40.7580, 40.7306, 40.7128],
    'Longitude': [-74.0060, -73.9712, -74.0060, -73.9352, -73.9855, -73.9352, -73.9897, -73.9855, -73.9352, -74.0060]
}

df = pd.DataFrame(data)

# Define features and targets
X = df[['GDP Growth Rate (%)', 'Unemployment Rate (%)', 'Living Conditions Index']]
y_migrants = df['Number of Migrants']
neighborhoods = df['Neighborhood']
coords = df[['Latitude', 'Longitude']]

# Split the data into training and testing sets
X_train, X_test, y_train_migrants, y_test_migrants = train_test_split(
    X, y_migrants, test_size=0.2, random_state=0
)

# Create and train the model
pipeline_migrants = make_pipeline(
    StandardScaler(),
    LinearRegression()
)
pipeline_migrants.fit(X_train, y_train_migrants)

# Predict number of migrants for the entire dataset
df['Predicted Migrants'] = pipeline_migrants.predict(X)

# Streamlit app
st.title('Neighborhood Population Change Prediction Due to Migration')

# Display predictions
st.write("### Predicted Number of Migrants by Neighborhood")
st.write(df[['Neighborhood', 'Predicted Migrants']])

# Visualization: Bar chart for number of migrants
fig_migrants, ax_migrants = plt.subplots()
ax_migrants.bar(df['Neighborhood'], df['Predicted Migrants'], color='blue')
ax_migrants.set_ylabel('Number of Predicted Migrants')
ax_migrants.set_title('Predicted Number of Migrants by Neighborhood')
plt.xticks(rotation=45)
st.pyplot(fig_migrants)

# Visualization: Map with HeatMap
m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)
heat_data = [[row['Latitude'], row['Longitude'], row['Predicted Migrants']] for index, row in df.iterrows()]
HeatMap(heat_data).add_to(m)

# Save map to HTML file and display it in Streamlit
map_html = 'map.html'
m.save(map_html)
with open(map_html, 'r') as f:
    st.components.v1.html(f.read(), height=500)

# Optionally, display model performance on test set
y_pred_migrants = pipeline_migrants.predict(X_test)
mse = mean_squared_error(y_test_migrants, y_pred_migrants)

st.write("### Model Evaluation")
st.write(f"Mean Squared Error for Number of Migrants: {mse:.2f}")
