# 09-fitness-data-analysis

# Cycling Dashboard

This cycling dashboard is an interactive web application that allows you to create personalized cycling dashboards from .tcx or .gpx files, which you can download from various sources, including Strava. With the cycling dashboard, you can visualize and analyze your cycling data in a user-friendly and informative way.

There are two options to view use this, the first is to clone this repo. It is also online at this [link](https://cycling-dashboard-3d5bfb76be1b.herokuapp.com/) (please bear in mind that load times are longer, especially for maps).

## Contents
- [Features](#features)
- [Getting Started](#getting-started)
   - [Requirements](#requirements)
   - [Installation](#installation)
- [Sourcing data](#sourcing-data)
    - [Strava](#strava)
- [Usage](#usage)

## Features

- **Dashboard Creation**: Upload .tcx files from your cycling activities and generate a comprehensive dashboard.

- **Data Visualization**: Utilizes Plotly for creating interactive and visually appealing charts, such as time-speed graphs and altitude-distance-speed graphs.

- **Mapping Your Ride**: Uses Folium to display your cycling route on an interactive map.

- **Data Preparation**: Leverages Pandas for data preprocessing, cleaning, and feature engineering from your raw cycling data.

## Getting Started

### Requirements

- Python 3.x
- Flask
- Plotly
- Folium
- Pandas

### Installation

1. Clone this repository
2. Change to the project directory:
3. Install the required packages:
4. Run the application

   ```bash
   python main.py

## Sourcing Data

### Strava
1. Head to www.strava.com and log in
2. On the dashboard, click here on the left:
   ![Alt text](info/strava/1.png)
3. Select an activity:
   ![Alt text](info/strava/2.png)
4. Click to open the menu, and export GPX:
   ![Alt text](info/strava/3.png)
   
## Usage

1. **Data**: On the web application, upload your .tcx or .gpx file in the upload OR, if you do not have data, choose one of the three radio selections to see sample data.

2. **Explore Your Data**: Interact with the generated dashboard:
   - **Key Statistics**: View the key statistics from the ride, such as date and time, total distance, total time, total ascent and average and maximum speeds.
   - **Interactive Charts**: Two charts with adjustable options. Use the dropdowns underneath to change the x and y axis in the left-most chart, and select either the distance or time for the x axis on the right-most chart.
   - **Interactive Map**: View an interactive map with your route plotted.
   - **Comparisons**: See how your ride compares against differents routes, peaks and animals.
