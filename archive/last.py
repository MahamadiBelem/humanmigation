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

# Extended dataset including additional demographic data
data = {
    'Neighborhood': ['Downtown', 'Uptown', 'Suburb', 'Countryside', 'Historic District', 
                      'Central', 'Old Town', 'New Town', 'Industrial Zone', 'Riverside'],
    'GDP Growth Rate (%)': [3.5, 2.1, 4.0, 1.5, 3.0, 2.8, 3.2, 3.9, 4.5, 2.0],
    'Unemployment Rate (%)': [5.0, 6.5, 4.2, 7.0, 5.8, 6.0, 5.5, 4.9, 3.8, 6.2],
    'Living Conditions Index': [70, 60, 80, 50, 65, 55, 75, 85, 90, 60],
    'Number of Migrants': [5000, 3000, 6000, 2000, 4000, 3500, 5500, 6500, 7000, 2500],
    'Age Distribution 0-18 (%)': [25, 20, 30, 15, 20, 18, 28, 35, 40, 22],
    'Age Distribution 19-64 (%)': [65, 60, 55, 70, 60, 62, 58, 55, 50, 65],
    'Age Distribution 65+ (%)': [10, 20, 15, 15, 20, 20, 14, 10, 10, 13],
    'Gender Ratio (Male/Female)': [1.05, 0.98, 1.10, 1.02, 0.95, 1.00, 1.07, 1.12, 1.08, 1.01],
    'Single-Parent Families (%)': [12, 15, 10, 8, 18, 14, 13, 12, 16, 11],
    'Latitude': [40.7128, 40.7831, 40.7128, 40.7306, 40.7580, 40.7306, 40.7411, 40.7580, 40.7306, 40.7128],
    'Longitude': [-74.0060, -73.9712, -74.0060, -73.9352, -73.9855, -73.9352, -73.9897, -73.9855, -73.9352, -74.0060]
}

df = pd.DataFrame(data)

# Define features and targets
X = df[['GDP Growth Rate (%)', 'Unemployment Rate (%)', 'Living Conditions Index']]
y_migrants = df['Number of Migrants']
y_age_dist_0_18 = df['Age Distribution 0-18 (%)']
y_age_dist_19_64 = df['Age Distribution 19-64 (%)']
y_age_dist_65 = df['Age Distribution 65+ (%)']
y_gender_ratio = df['Gender Ratio (Male/Female)']
y_single_parent_families = df['Single-Parent Families (%)']

# Split the data into training and testing sets for predictions
X_train, X_test, y_train_migrants, y_test_migrants = train_test_split(
    X, y_migrants, test_size=0.2, random_state=0
)
X_train, X_test, y_train_age_dist_0_18, y_test_age_dist_0_18 = train_test_split(
    X, y_age_dist_0_18, test_size=0.2, random_state=0
)
X_train, X_test, y_train_age_dist_19_64, y_test_age_dist_19_64 = train_test_split(
    X, y_age_dist_19_64, test_size=0.2, random_state=0
)
X_train, X_test, y_train_age_dist_65, y_test_age_dist_65 = train_test_split(
    X, y_age_dist_65, test_size=0.2, random_state=0
)
X_train, X_test, y_train_gender_ratio, y_test_gender_ratio = train_test_split(
    X, y_gender_ratio, test_size=0.2, random_state=0
)
X_train, X_test, y_train_single_parent_families, y_test_single_parent_families = train_test_split(
    X, y_single_parent_families, test_size=0.2, random_state=0
)

# Create and train the models
pipeline_migrants = make_pipeline(
    StandardScaler(),
    LinearRegression()
)
pipeline_migrants.fit(X_train, y_train_migrants)

pipeline_age_dist_0_18 = make_pipeline(
    StandardScaler(),
    LinearRegression()
)
pipeline_age_dist_0_18.fit(X_train, y_train_age_dist_0_18)

pipeline_age_dist_19_64 = make_pipeline(
    StandardScaler(),
    LinearRegression()
)
pipeline_age_dist_19_64.fit(X_train, y_train_age_dist_19_64)

pipeline_age_dist_65 = make_pipeline(
    StandardScaler(),
    LinearRegression()
)
pipeline_age_dist_65.fit(X_train, y_train_age_dist_65)

pipeline_gender_ratio = make_pipeline(
    StandardScaler(),
    LinearRegression()
)
pipeline_gender_ratio.fit(X_train, y_train_gender_ratio)

pipeline_single_parent_families = make_pipeline(
    StandardScaler(),
    LinearRegression()
)
pipeline_single_parent_families.fit(X_train, y_train_single_parent_families)

# Predict for the entire dataset
df['Predicted Migrants'] = pipeline_migrants.predict(X)
df['Predicted Age Distribution 0-18 (%)'] = pipeline_age_dist_0_18.predict(X)
df['Predicted Age Distribution 19-64 (%)'] = pipeline_age_dist_19_64.predict(X)
df['Predicted Age Distribution 65+ (%)'] = pipeline_age_dist_65.predict(X)
df['Predicted Gender Ratio (Male/Female)'] = pipeline_gender_ratio.predict(X)
df['Predicted Single-Parent Families (%)'] = pipeline_single_parent_families.predict(X)

# Streamlit app
st.title('Population Change Prediction Due to Migration and Demographic Analysis')

# Display predictions
st.write("### Predicted Population Changes and Demographic Shifts")
st.write(df[['Neighborhood', 'Predicted Migrants', 'Predicted Age Distribution 0-18 (%)', 
            'Predicted Age Distribution 19-64 (%)', 'Predicted Age Distribution 65+ (%)', 
            'Predicted Gender Ratio (Male/Female)', 'Predicted Single-Parent Families (%)']])

# Visualization: Bar charts for predicted demographic changes
fig_demographics, axs = plt.subplots(3, 2, figsize=(14, 12))
fig_demographics.suptitle('Predicted Demographic Changes by Neighborhood')

# Number of Migrants
axs[0, 0].bar(df['Neighborhood'], df['Predicted Migrants'], color='blue')
axs[0, 0].set_ylabel('Number of Migrants')
axs[0, 0].set_title('Predicted Number of Migrants')
axs[0, 0].tick_params(axis='x', rotation=45)

# Age Distribution 0-18
axs[0, 1].bar(df['Neighborhood'], df['Predicted Age Distribution 0-18 (%)'], color='orange')
axs[0, 1].set_ylabel('Age Distribution 0-18 (%)')
axs[0, 1].set_title('Predicted Age Distribution 0-18')
axs[0, 1].tick_params(axis='x', rotation=45)

# Age Distribution 19-64
axs[1, 0].bar(df['Neighborhood'], df['Predicted Age Distribution 19-64 (%)'], color='green')
axs[1, 0].set_ylabel('Age Distribution 19-64 (%)')
axs[1, 0].set_title('Predicted Age Distribution 19-64')
axs[1, 0].tick_params(axis='x', rotation=45)

# Age Distribution 65+
axs[1, 1].bar(df['Neighborhood'], df['Predicted Age Distribution 65+ (%)'], color='red')
axs[1, 1].set_ylabel('Age Distribution 65+ (%)')
axs[1, 1].set_title('Predicted Age Distribution 65+')
axs[1, 1].tick_params(axis='x', rotation=45)

# Gender Ratio
axs[2, 0].bar(df['Neighborhood'], df['Predicted Gender Ratio (Male/Female)'], color='purple')
axs[2, 0].set_ylabel('Gender Ratio (Male/Female)')
axs[2, 0].set_title('Predicted Gender Ratio')
axs[2, 0].tick_params(axis='x', rotation=45)

# Single-Parent Families
axs[2, 1].bar(df['Neighborhood'], df['Predicted Single-Parent Families (%)'], color='brown')
axs[2, 1].set_ylabel('Single-Parent Families (%)')
axs[2, 1].set_title('Predicted Single-Parent Families')
axs[2, 1].tick_params(axis='x', rotation=45)

plt.tight_layout(rect=[0, 0, 1, 0.95])
st.pyplot(fig_demographics)

# Visualization: Map with HeatMap for predicted migrants
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
y_pred_age_dist_0_18 = pipeline_age_dist_0_18.predict(X_test)
y_pred_age_dist_19_64 = pipeline_age_dist_19_64.predict(X_test)
y_pred_age_dist_65 = pipeline_age_dist_65.predict(X_test)
y_pred_gender_ratio = pipeline_gender_ratio.predict(X_test)
y_pred_single_parent_families = pipeline_single_parent_families.predict(X_test)

mse_migrants = mean_squared_error(y_test_migrants, y_pred_migrants)
mse_age_dist_0_18 = mean_squared_error(y_test_age_dist_0_18, y_pred_age_dist_0_18)
mse_age_dist_19_64 = mean_squared_error(y_test_age_dist_19_64, y_pred_age_dist_19_64)
mse_age_dist_65 = mean_squared_error(y_test_age_dist_65, y_pred_age_dist_65)
mse_gender_ratio = mean_squared_error(y_test_gender_ratio, y_pred_gender_ratio)
mse_single_parent_families = mean_squared_error(y_test_single_parent_families, y_pred_single_parent_families)

st.write("### Model Evaluation")
st.write(f"Mean Squared Error for Number of Migrants: {mse_migrants:.2f}")
st.write(f"Mean Squared Error for Age Distribution 0-18: {mse_age_dist_0_18:.2f}")
st.write(f"Mean Squared Error for Age Distribution 19-64: {mse_age_dist_19_64:.2f}")
st.write(f"Mean Squared Error for Age Distribution 65+: {mse_age_dist_65:.2f}")
st.write(f"Mean Squared Error for Gender Ratio: {mse_gender_ratio:.2f}")
st.write(f"Mean Squared Error for Single-Parent Families: {mse_single_parent_families:.2f}")
