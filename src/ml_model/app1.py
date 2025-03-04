# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import folium
# import streamlit.components.v1 as components

# # Title of the application
# st.title("Earthquake Data Analysis")
# shakemap_ = pd.read_csv("C:\\Users\\nagar\\OneDrive\\Desktop\\all\\ML\\shakemap.csv")

# # Sidebar for dataset selection
# plot_type = st.sidebar.selectbox("Select Plot Type", ["Time Series", "Scatter Geo Map"])

# if plot_type == "Time Series":
#     dataset = st.sidebar.selectbox("Select Dataset", ["Japan", "Haiti", "Iraq-Iran", "Turkey", "Mexico"])

#     # Load data based on selection and define color/title
#     data = {
#         "Japan": {
#             "path": 'C:\\Users\\nagar\\OneDrive\\Desktop\\all\\ML\\classsfy_model_data\\japan_predictions.csv',
#             "color": 'green',
#             "title": "Time Series Line Chart of Japan Earthquake Tweets"
#         },
#         "Haiti": {
#             "path": 'C:\\Users\\nagar\\OneDrive\\Desktop\\all\\ML\\classsfy_model_data\\haiti_predictions.csv',
#             "color": 'blue',
#             "title": "Time Series Line Chart of Haiti Earthquake Tweets"
#         },
#         "Iraq-Iran": {
#             "path": 'C:\\Users\\nagar\\OneDrive\\Desktop\\all\\ML\\classsfy_model_data\\iraq_iran_predictions.csv',
#             "color": 'red',
#             "title": "Time Series Line Chart of Iraq-Iran Earthquake Tweets"
#         },
#         "Turkey": {
#             "path": 'C:\\Users\\nagar\\OneDrive\\Desktop\\all\\ML\\classsfy_model_data\\turkey_predictions (1).csv',
#             "color": 'orange',
#             "title": "Time Series Line Chart of Turkey Earthquake Tweets"
#         },
#         "Mexico": {
#             "path": 'C:\\Users\\nagar\\OneDrive\\Desktop\\all\\ML\\classsfy_model_data\\maxico_predictions.csv',
#             "color": 'purple',
#             "title": "Time Series Line Chart of Mexico Earthquake Tweets"
#         }
#     }

#     # Load the selected dataset
#     data_info = data[dataset]  # Corrected from data_map to data

#     # Load the data from the CSV file
#     data = pd.read_csv(data_info["path"])

#     # Group data by date
#     data_grouped = data.groupby('date').count().reset_index()

#     # Determine the size of the figure based on the number of data points
#     num_points = len(data_grouped)
#     if num_points <= 100:
#         fig_width = 600
#         fig_height = 400
#     elif num_points <= 1000:
#         fig_width = 800
#         fig_height = 500
#     elif num_points <= 10000:
#         fig_width = 1000
#         fig_height = 600
#     elif num_points <= 50000:
#         fig_width = 1200
#         fig_height = 700
#     elif num_points <= 100000:
#         fig_width = 1400
#         fig_height = 800
#     else:
#         fig_width = 1600
#         fig_height = 900

#     # Create a Plotly figure for time series
#     fig_time_series = px.line(data_grouped, x='date', y='text', title=data_info["title"], 
#                                labels={'text': 'Number of Tweets in a Day', 'date': 'Dates'},
#                                line_shape='linear')
#     fig_time_series.update_traces(line=dict(color=data_info["color"]), mode='lines+markers')

#     # Update layout for time series plot
#     fig_time_series.update_layout(width=fig_width, height=fig_height,
#                                   xaxis_title="Dates",
#                                   yaxis_title="Number of Tweets in a Day",
#                                   xaxis=dict(tickformat="%Y-%m-%d"),
#                                   xaxis_tickangle=-45)

#     # Show the time series plot in Streamlit
#     st.plotly_chart(fig_time_series)

# elif plot_type == "Scatter Geo Map":
#     # Create a Folium map centered at a general location
#     m = folium.Map(location=[20, 0], zoom_start=2)

#     # Function to determine marker color based on magnitude
#     def get_marker_color(magnitude):
#         if magnitude >= 9:
#             return 'red'
#         elif magnitude >= 8:
#             return 'yellow'
#         else:
#             return 'green'

#     # Add circle markers to the map for each earthquake
#     for _, entry in shakemap_.iterrows():
#         magnitude = entry['mag']
#         color = get_marker_color(magnitude)

#         folium.CircleMarker(
#             location=[entry['latitude'], entry['longitude']],
#             radius=2,
#             popup=f"Mag: {magnitude}",
#             color=color,
#             fill=True,
#             fill_color=color,
#             fill_opacity=0.4
#         ).add_to(m)

#     # Save the map to an HTML file
#     map_html = "temp_map.html"
#     m.save(map_html)

#     # Display the map in Streamlit
#     with open(map_html, 'r', encoding='utf-8') as f:
#         map_html_data = f.read()
#     components.html(map_html_data, height=600)
