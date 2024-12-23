import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Static Data for Metadata (Simulating MongoDB records)
metadata_data = [
    {"type": "dataset", "name": "Migration Data"},
    {"type": "dataset", "name": "Factors Data"},
    {"type": "dataset", "name": "Spatiale Data"},
    {"type": "other", "name": "Document 1"},
    {"type": "other", "name": "Document 2"},
    {"type": "other", "name": "Document 3"},
]

# Static Data for Migration Data (Yearly migration count)
migration_data = [
    {"Year": 2015, "Migrants": 5000},
    {"Year": 2016, "Migrants": 6000},
    {"Year": 2017, "Migrants": 7000},
    {"Year": 2018, "Migrants": 7500},
    {"Year": 2019, "Migrants": 8000},
    {"Year": 2020, "Migrants": 8500},
    {"Year": 2021, "Migrants": 9000},
]

# Function to simulate the count of datasets and other records
def get_record_counts():
    dataset_count = sum(1 for record in metadata_data if record['type'] == "dataset")
    other_count = sum(1 for record in metadata_data if record['type'] != "dataset")
    return dataset_count, other_count

# Function to simulate fetching migration data by year
def get_migration_data_by_year():
    return pd.DataFrame(migration_data)

# Display Record Counts
def display_record_counts():
    dataset_count, other_count = get_record_counts()
    st.write(f"### Number of Datasets: {dataset_count}")
    st.write(f"### Number of Other Records: {other_count}")

# Visualize Migration Data by Year
def visualize_migration_by_year():
    migration_df = get_migration_data_by_year()
    st.write("### Migration Trends Over Time")
    
    if not migration_df.empty:
        st.line_chart(migration_df.set_index('Year')['Migrants'])
    else:
        st.write("No data available.")



# Simulating migration data by region
migration_by_region = [
    {"Year": 2015, "Region": "Africa", "Migrants": 1000},
    {"Year": 2015, "Region": "Asia", "Migrants": 1500},
    {"Year": 2016, "Region": "Africa", "Migrants": 1200},
    {"Year": 2016, "Region": "Asia", "Migrants": 1700},
    {"Year": 2017, "Region": "Africa", "Migrants": 1300},
    {"Year": 2017, "Region": "Asia", "Migrants": 1800},
    {"Year": 2018, "Region": "Africa", "Migrants": 1400},
    {"Year": 2018, "Region": "Asia", "Migrants": 1900},
    {"Year": 2019, "Region": "Africa", "Migrants": 1500},
    {"Year": 2019, "Region": "Asia", "Migrants": 2000},
]

# Function to visualize migration by region
def visualize_migration_by_region():
    region_df = pd.DataFrame(migration_by_region)
    st.write("### Migration by Region Over Time")
    region_pivot = region_df.pivot_table(values='Migrants', index='Year', columns='Region', aggfunc='sum')
    st.line_chart(region_pivot)

# visualize_migration_by_region()



# Simulating migration data with age group and education level
migration_with_demographics = [
    {"Year": 2015, "Age Group": "18-25", "Education Level": "Bachelor", "Migrants": 2000},
    {"Year": 2015, "Age Group": "26-35", "Education Level": "Master", "Migrants": 1500},
    {"Year": 2016, "Age Group": "18-25", "Education Level": "Bachelor", "Migrants": 2500},
    {"Year": 2016, "Age Group": "26-35", "Education Level": "Master", "Migrants": 1800},
    {"Year": 2017, "Age Group": "18-25", "Education Level": "Bachelor", "Migrants": 2200},
    {"Year": 2017, "Age Group": "26-35", "Education Level": "Master", "Migrants": 1700},
]

# Function to visualize migration by age group and education level
def visualize_migration_by_age_and_education():
    demo_df = pd.DataFrame(migration_with_demographics)
    st.write("### Migration by Age Group and Education Level")
    demo_pivot = demo_df.pivot_table(values='Migrants', index='Age Group', columns='Education Level', aggfunc='sum')
    st.bar_chart(demo_pivot)

# visualize_migration_by_age_and_education()


# Simulating factors data (e.g., investment or job availability)
factors_data = [
    {"Factor": "Investment", "Value": 1000, "Migrants": 5000},
    {"Factor": "Investment", "Value": 1500, "Migrants": 6000},
    {"Factor": "Job Availability", "Value": 2000, "Migrants": 7000},
    {"Factor": "Job Availability", "Value": 2500, "Migrants": 8000},
]

# Function to visualize impact of factors on migration
def visualize_impact_of_factors():
    factors_df = pd.DataFrame(factors_data)
    st.write("### Impact of Factors on Migration")
    factors_grouped = factors_df.groupby('Factor').agg({'Migrants': 'sum', 'Value': 'mean'}).reset_index()
    st.bar_chart(factors_grouped.set_index('Factor')['Migrants'])

# visualize_impact_of_factors()


# Simulating migration data with ratings
migration_with_rating = [
    {"Year": 2015, "Country": "A", "Rating": 4.5, "Migrants": 1000},
    {"Year": 2016, "Country": "B", "Rating": 4.7, "Migrants": 1500},
    {"Year": 2017, "Country": "A", "Rating": 4.8, "Migrants": 2000},
    {"Year": 2018, "Country": "B", "Rating": 4.6, "Migrants": 2500},
]

# Function to visualize correlation between migration and rating
def visualize_migration_and_rating():
    rating_df = pd.DataFrame(migration_with_rating)
    st.write("### Correlation Between Migration and Country Rating")
    st.scatter_chart(rating_df.set_index('Year')[['Migrants', 'Rating']])

# visualize_migration_and_rating()


# Simulating country-to-country migration flow
migration_flow_data = [
    {"From": "Country A", "To": "Country B", "Migrants": 1000},
    {"From": "Country B", "To": "Country A", "Migrants": 1200},
    {"From": "Country A", "To": "Country C", "Migrants": 800},
    {"From": "Country C", "To": "Country A", "Migrants": 700},
]

# Function to visualize migration flow
def visualize_migration_flow():
    flow_df = pd.DataFrame(migration_flow_data)
    st.write("### Migration Flow Between Countries")
    flow_pivot = flow_df.pivot_table(values='Migrants', index='From', columns='To', aggfunc='sum').fillna(0)
    st.write(flow_pivot)

# visualize_migration_flow()



# Simulated migration flow data between Burkina Faso, Ivory Coast, Mali, and Italy
migration_data_fl = {
    "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021],
    "Burkina Faso to Italy": [500, 600, 700, 800, 900, 1000, 1100],
    "Ivory Coast to Italy": [1500, 1600, 1700, 1800, 1900, 2000, 2100],
    "Mali to Italy": [1200, 1300, 1400, 1500, 1600, 1700, 1800],
    "Italy to Burkina Faso": [200, 250, 300, 350, 400, 450, 500],
    "Italy to Ivory Coast": [800, 850, 900, 950, 1000, 1050, 1100],
    "Italy to Mali": [700, 750, 800, 850, 900, 950, 1000]
}

# Convert data to a DataFrame
migration_df = pd.DataFrame(migration_data_fl)

# Set the 'Year' as the index
migration_df.set_index("Year", inplace=True)

# Function to visualize Migration Flow as a Line Chart
def visualize_migration_flow_fl():
    st.write("### Migration Flow Over Time (From Burkina Faso, Ivory Coast, Mali to Italy)")

    # Streamlit widget to select which migration flow to display
    countries = [
        "Burkina Faso to Italy",
        "Ivory Coast to Italy",
        "Mali to Italy",
        "Italy to Burkina Faso",
        "Italy to Ivory Coast",
        "Italy to Mali"
    ]
    
    # User selects which migration flow to view
    selected_country = st.selectbox("Select Migration Flow:", countries)

    # Filter data based on selected country
    selected_data = migration_df[[selected_country]]

    # Display line chart for selected migration flow
    st.line_chart(selected_data)

    # Display additional details on hover (tooltips)
    st.write(f"#### Detailed Migration Flow: {selected_country}")
    st.write(selected_data)



# Call the function to visualize migration flow
# visualize_migration_flow()




# Static data for testing
def get_static_data(query_type):
    # Simulate query results based on the query type
    if query_type == "group_by_location":
        # Grouped data by location with counts
        return [
            {"_id": "Burkina Faso", "count": 150},
            {"_id": "Ivory Coast", "count": 200},
            {"_id": "Mali", "count": 100},
            {"_id": "Italy", "count": 250}
        ]
    
    elif query_type == "migration_by_year":
        # Migration data over the years
        return [
            {"_id": 2015, "total_migrants": 5000},
            {"_id": 2016, "total_migrants": 6000},
            {"_id": 2017, "total_migrants": 7000},
            {"_id": 2018, "total_migrants": 8000},
            {"_id": 2019, "total_migrants": 9000}
        ]

    else:
        return []

# Function to plot bar chart for grouped data
def plot_bar_chart(data, x_col, y_col):
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x=x_col, y=y_col, palette="Blues_d")
    plt.title(f"{y_col} by {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    st.pyplot(plt)

# Function to plot line chart for time series data
def plot_line_chart(data, x_col, y_col):
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x=x_col, y=y_col, marker="o", color="b")
    plt.title(f"{y_col} over {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    st.pyplot(plt)

# Streamlit app layout
def main_execute_query():
    # Provide instructions
    st.write("### Choose a MongoDB query to execute or write your own")
    
    # Dropdown to select predefined queries
    query_type = st.selectbox("Select a predefined query", [
        "count_datasets", 
        "count_non_datasets", 
        "group_by_location", 
        "migration_by_year"
    ])

    # Get static data for the selected query type
    query_str = ""
    if query_type == "count_datasets":
        query_str = "metadata_collection.count_documents({'type': 'dataset'})"
    elif query_type == "count_non_datasets":
        query_str = "metadata_collection.count_documents({'type': {'$ne': 'dataset'}})"
    elif query_type == "group_by_location":
        query_str = "metadata_collection.aggregate([{'$group': {'_id': '$Location', 'count': {'$sum': 1}}}])"
    elif query_type == "migration_by_year":
        query_str = "metadata_collection.aggregate([{'$match': {'Type': 'dataset'}}, {'$group': {'_id': '$Year', 'total_migrants': {'$sum': '$Migrants'}}}, {'$sort': {'_id': 1}}])"

    # Display the query string in a text box where users can modify it if needed
    query_input = st.text_area("Edit your MongoDB query", value=query_str, height=200)

    # Execute the query when the user presses the button
    if st.button("Execute Query"):
        # For testing purposes, we simulate the query result from static data
        result = get_static_data(query_type)
        st.write("### Query Result:")
        st.write(result)

        # If the result is a list of documents (for aggregation results), plot the graphs
        if isinstance(result, list) and len(result) > 0:
            # Determine what kind of data we're dealing with
            if query_type == "group_by_location" or query_type == "migration_by_year":
                graph_type = st.selectbox("Select Graph Type", ["Bar Chart", "Line Chart"])

                if graph_type == "Bar Chart":
                    # Plot a bar chart (grouped data like counts)
                    plot_bar_chart(result, x_col="_id", y_col="count" if query_type == "group_by_location" else "total_migrants")
                
                elif graph_type == "Line Chart":
                    # Plot a line chart (time-series data like migration over years)
                    plot_line_chart(result, x_col="_id", y_col="total_migrants" if query_type == "migration_by_year" else "count")





# import streamlit as st
# import pymongo
# import matplotlib.pyplot as plt
# import pandas as pd
# import seaborn as sns

# # Function to execute MongoDB queries
# def execute_mongo_query(query_str):
#     client = pymongo.MongoClient("mongodb://localhost:27017")
#     db = client["test_finale_db"]  # Replace with your database name
#     metadata_collection = db["metadata"]  # Replace with your collection name

#     try:
#         # Use eval() to execute the query (Note: Be careful with eval in production code!)
#         result = eval(query_str)
#         return result
#     except Exception as e:
#         return f"Error: {e}"

# # Function to provide the predefined queries
# def get_predefined_query(query_type):
#     queries = {
#         "count_datasets": "metadata_collection.count_documents({'type': 'dataset'})",
#         "count_non_datasets": "metadata_collection.count_documents({'type': {'$ne': 'dataset'}})",
#         "group_by_location": """
# metadata_collection.aggregate([
#     {"$group": {"_id": "$Location", "count": {"$sum": 1}}}
# ])""",
#         "migration_by_year": """
# metadata_collection.aggregate([
#     {"$match": {"Type": "dataset"}},
#     {"$group": {"_id": "$Year", "total_migrants": {"$sum": "$Migrants"}}},
#     {"$sort": {"_id": 1}}
# ])"""
#     }
#     return queries.get(query_type, "")

# # Function to plot bar chart for grouped data
# def plot_bar_chart(data, x_col, y_col):
#     df = pd.DataFrame(data)
#     plt.figure(figsize=(10, 6))
#     sns.barplot(data=df, x=x_col, y=y_col, palette="Blues_d")
#     plt.title(f"{y_col} by {x_col}")
#     plt.xlabel(x_col)
#     plt.ylabel(y_col)
#     st.pyplot(plt)

# # Function to plot line chart for time series data
# def plot_line_chart(data, x_col, y_col):
#     df = pd.DataFrame(data)
#     plt.figure(figsize=(10, 6))
#     sns.lineplot(data=df, x=x_col, y=y_col, marker="o", color="b")
#     plt.title(f"{y_col} over {x_col}")
#     plt.xlabel(x_col)
#     plt.ylabel(y_col)
#     st.pyplot(plt)

# # Streamlit app layout
# def main():
#     st.title("MongoDB Query Executor with Graph Options")

#     # Provide instructions
#     st.write("### Choose a MongoDB query to execute")
#     query_type = st.selectbox("Select a query", [
#         "count_datasets", 
#         "count_non_datasets", 
#         "group_by_location", 
#         "migration_by_year"
#     ])

#     # Get the corresponding query string for the selected query
#     query_str = get_predefined_query(query_type)

#     # Display the query string in a text box where users can modify it if needed
#     query_input = st.text_area("Edit your MongoDB query", value=query_str, height=200)

#     # Execute the query when the user presses the button
#     if st.button("Execute Query"):
#         result = execute_mongo_query(query_input)
#         st.write("### Query Result:")
#         st.write(result)

#         # If the result is a list of documents (for aggregation results), plot the graphs
#         if isinstance(result, list) and len(result) > 0:
#             # Determine what kind of data we're dealing with
#             if query_type == "group_by_location" or query_type == "migration_by_year":
#                 graph_type = st.selectbox("Select Graph Type", ["Bar Chart", "Line Chart"])

#                 if graph_type == "Bar Chart":
#                     # Plot a bar chart (grouped data like counts)
#                     plot_bar_chart(result, x_col="_id", y_col="count" if query_type == "group_by_location" else "total_migrants")
                
#                 elif graph_type == "Line Chart":
#                     # Plot a line chart (time-series data like migration over years)
#                     plot_line_chart(result, x_col="_id", y_col="total_migrants" if query_type == "migration_by_year" else "count")

# if __name__ == "__main__":
#     main()







import streamlit as st
from streamlit_option_menu import option_menu

# Import your functions for each visualization or analysis
# from your_module import main_execute_query, display_record_counts, visualize_migration_by_year, etc.

def home_request():
        # Sidebar for navigation using streamlit-option-menu
    with st.sidebar:
            # Create an option menu in the sidebar
            choice = option_menu(
                menu_title="Select Data to Visualize",  # Sidebar menu title
                options=[
                    "Query data", "Dataset Counts", "Migration Trends", 
                    "Migration by Region", "Demographics", "Factors Impact", 
                    "Migration and Rating", "Migration Flow", "Migration per Country"
                ],
                icons=["database", "list", "graph-up", "globe", "person", "bar-chart", "star", "arrow-right", "flag"],
                menu_icon="cast",  # Optional icon for the menu
                default_index=0,  # Default option selected
                orientation="vertical"  # Menu orientation (vertical in the sidebar)
            )
        
        # Now, call the appropriate function based on the selected option
    if choice == "Query data":
            main_execute_query()
    elif choice == "Dataset Counts":
            display_record_counts()
    elif choice == "Migration Trends":
            visualize_migration_by_year()
    elif choice == "Migration by Region":
            visualize_migration_by_region()
    elif choice == "Demographics":
            visualize_migration_by_age_and_education()
    elif choice == "Factors Impact":
            visualize_impact_of_factors()
    elif choice == "Migration and Rating":
            visualize_migration_and_rating()
    elif choice == "Migration Flow":
            visualize_migration_flow()
    elif choice == "Migration per Country":
            visualize_migration_flow_fl()





# def main_static_test_data():
#     # Sidebar for navigation
#     st.sidebar.title("Select Data to Visualize")
#     choice = st.sidebar.radio("Choose an option:", ["Query data","Dataset Counts", "Migration Trends", "Migration by Region", "Demographics", "Factors Impact", "Migration and Rating", "Migration Flow","Migration per country"])

#     if choice == "Query data":
#         main_execute_query()
#     if choice == "Dataset Counts":
#         display_record_counts()
#     elif choice == "Migration Trends":
#         visualize_migration_by_year()
#     elif choice == "Migration by Region":
#         visualize_migration_by_region()
#     elif choice == "Demographics":
#         visualize_migration_by_age_and_education()
#     elif choice == "Factors Impact":
#         visualize_impact_of_factors()
#     elif choice == "Migration and Rating":
#         visualize_migration_and_rating()
#     elif choice == "Migration Flow":
#         visualize_migration_flow()
#     elif choice == "Migration per country":
#         visualize_migration_flow_fl()



# if __name__ == "__main__":
#     main_static_test_data()









