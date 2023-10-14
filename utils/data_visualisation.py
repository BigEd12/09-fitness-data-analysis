import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium

from utils import data_preparation

def time_distance_graph(df):    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['Total Time (M)'], y=df['Total Distance (M)'],
                   line=dict(width=1, color='#6CE5E8'),
                   hoverinfo='text',
                   text=['Time={} min, Distance={} Km'.format(round(time, 1), round(distance / 1000, 2))
                              for i, (time, distance) in enumerate(zip(df['Total Time (M)'], df['Total Distance (M)']))],
                   mode='lines+markers',
                   )
    )
    
    x_lims = df.iloc[-1]['Total Time (M)'] * 1.1
    y_lims = df.iloc[-1]['Total Distance (M)'] * 1.1
    

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)

    fig.update_xaxes(title_text='Time (minutes)', range=[0, x_lims])
    fig.update_yaxes(title_text='Distance (Km)', range=[0, y_lims])

    fig.update_layout(title_text='Time - Distance')
    
    fig.update_layout(
        plot_bgcolor='#0B2447',
        paper_bgcolor='#0B2447',
        xaxis=dict(showgrid=False, gridcolor='#6CE5E8', title_font=dict(color='white'), tickfont=dict(color='white')),
        yaxis=dict(showgrid=False, gridcolor='#6CE5E8', title_font=dict(color='white'), tickfont=dict(color='white')),
    )
    
    fig.update_traces(
        hoverlabel=dict(
            bgcolor='#123C76',
            bordercolor='#123C76',
            font=dict(size=14, color='white'),
        )
    )
    
    fig.update_layout(
        title_font=dict(color='white'),
    )

    save_name = "temp/time_distance_graph.html"
    
    fig.write_html(save_name)

    return save_name

def distance_altitude_graph(df):    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['Total Distance (M)'], y=df['Altitude (M)'],
                   line=dict(width=1, color='#6CE5E8'),
                   hoverinfo='text',
                   text=['Distance={} Km, Altitude={} M'.format(round(distance / 1000, 2, ), round(altitude, 2))
                              for i, (distance, altitude) in enumerate(zip(df['Total Distance (M)'], df['Altitude (M)']))],
                   mode='lines+markers',
                   )
    )
    
    x_lims = df.iloc[-1]['Total Distance (M)'] * 1.1
    y_lims = df['Altitude (M)'].max() * 1.1
    

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)

    fig.update_xaxes(title_text='Distance (Km)', range=[0, x_lims])
    fig.update_yaxes(title_text='Altitude (M)', range=[0, y_lims])

    fig.update_layout(title_text='Distance - Altitude')
    
    fig.update_layout(
        plot_bgcolor='#0B2447',
        paper_bgcolor='#0B2447',
        xaxis=dict(showgrid=False, gridcolor='#2D8BBA', title_font=dict(color='white'), tickfont=dict(color='white')),
        yaxis=dict(showgrid=False, gridcolor='#2D8BBA', title_font=dict(color='white'), tickfont=dict(color='white')),
    )
    
    fig.update_layout(
        title_font=dict(color='white'),
    )
    
    fig.update_traces(
        hoverlabel=dict(
            bgcolor='#123C76',
            bordercolor='#123C76',
            font=dict(size=14, color='white'),
        )
    )
    
    save_name = "temp/altitude_distance_chart.html"
    
    fig.write_html(save_name)

    return save_name


def time_altitude_graph(df):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['Total Time (M)'], y=df['Altitude (M)'],
                   line=dict(width=1, color='#6CE5E8'),
                   hoverinfo='text',
                   text=['Time={} min, Altitude={} M'.format(round(time, 2), round(altitude, 2))
                              for time, altitude in zip(df['Total Time (M)'], df['Altitude (M)'])],
                   mode='lines+markers',
                   )
    )

    x_lims = df.iloc[-1]['Total Time (M)'] * 1.1
    y_lims = df['Altitude (M)'].max() * 1.1

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)

    fig.update_xaxes(title_text='Time (min)', range=[0, x_lims])
    fig.update_yaxes(title_text='Altitude (M)', range=[0, y_lims])

    fig.update_layout(
        plot_bgcolor='#0B2447',
        paper_bgcolor='#0B2447',
        xaxis=dict(showgrid=False, gridcolor='#6CE5E8', title_font=dict(color='white'), tickfont=dict(color='white')),
        yaxis=dict(showgrid=False, gridcolor='#6CE5E8', title_font=dict(color='white'), tickfont=dict(color='white')),
    )

    fig.update_layout(
        title_text='Time - Altitude', 
        title_font=dict(color='white')
    )

    fig.update_traces(
    hoverlabel=dict(
        bgcolor='#123C76',
        bordercolor='#123C76',
        font=dict(size=14, color='white'),
    ))

    save_name = "temp/time_altitude_graph.html"
    
    fig.write_html(save_name)

    return save_name



def distance_speed_graph(df):
    fig = go.Figure()

    window_size = 6
    num_windows = len(df) // window_size

    avg_distances = []
    avg_speeds = []

    for i in range(num_windows):
        start_idx = i * window_size
        end_idx = (i + 1) * window_size

        avg_distance = df['Total Distance (M)'].iloc[start_idx:end_idx].mean()
        avg_speed = df['Segment Speed'].iloc[start_idx:end_idx].sum() / window_size

        avg_distances.append(avg_distance)
        avg_speeds.append(avg_speed)

    averaged_data = pd.DataFrame({'Distance': avg_distances, 'Speed': avg_speeds})

    
    fig.add_trace(
        go.Scatter(x=averaged_data['Distance'], y=averaged_data['Speed'],
                   mode='lines+markers',
                   marker=dict(size=4, color='#6CE5E8'),
                   name='Speed',
                   hoverinfo='text',
                   text=['Distance={:.2f} Km, Speed={:.2f} Km/h'.format(round(distance / 1000, 2), round(speed, 2)) for distance, speed in zip(avg_distances, avg_speeds)]
                   )
    )

    x_lims = df['Total Distance (M)'].max() * 1.01
    y_lims = df['Segment Speed'].max() * 1.1

    fig.update_layout(
        xaxis_showgrid=False, yaxis_showgrid=False,
        xaxis_title='Distance (Km)', yaxis_title='Speed (Km/h)',
        title_text='Speed over Distance',
        plot_bgcolor='#0B2447',
        paper_bgcolor='#0B2447'
    )

    fig.update_xaxes(range=[0, x_lims])
    fig.update_yaxes(range=[0, y_lims])
    
    
    average_speed = data_preparation.speed_info(df)[0]
    
    fig.add_shape(
        dict(
            type='line',
            x0=0,
            x1=x_lims,
            y0=average_speed,
            y1=average_speed,
            line=dict(color='#6CE5E8', width=2, dash='dash'),
            name='Average Speed Km/h',
        )
    )
    
    
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='#6CE5E8', width=2, dash='dash'), name='Average Speed Km/h', showlegend=True))

    max_speed_value, ms_id = data_preparation.highest_average_speed(df)
    max_speed_distance = df.iloc[ms_id]['Total Distance (KM)']
    max_speed_text = ['Highest Speed Obtained: Distance={} Km, Speed={} Km/h'.format(
                       round(df.iloc[df['Segment Speed'].idxmax()]['Total Distance (M)'] / 1000, 2), round(df['Segment Speed'].max(), 2)) for distance, speed in zip(avg_distances, avg_speeds)]
    fig.add_trace(
        go.Scatter(x=[max_speed_distance], y=[max_speed_value],
                   mode='markers',
                   marker=dict(size=12, color='#6CE5E8', symbol='diamond'),
                   hoverinfo='text',
                   text=max_speed_text,
                   name='Highest Speed',
                   )
    )
    
    fig.update_layout(
        plot_bgcolor='#0B2447',
        paper_bgcolor='#0B2447',
        xaxis=dict(showgrid=False, gridcolor='#2D8BBA', title_font=dict(color='white'), tickfont=dict(color='white')),
        yaxis=dict(showgrid=False, gridcolor='#2D8BBA', title_font=dict(color='white'), tickfont=dict(color='white')),
    )
    
    fig.update_traces(
        hoverlabel=dict(
            bgcolor='#123C76',
            bordercolor='#123C76',
            font=dict(size=14, color='white'),
        )
    )
    
    fig.update_layout(
        title_font=dict(color='white'),
        legend=dict(
        font=dict(
            color='white'
        )
    )
    )

    save_name = "temp/distance_speed_chart.html"
    
    fig.write_html(save_name)

    return save_name


def time_speed_graph(df):
    fig = go.Figure()

    avg_times = []
    avg_speeds = []

    for i in range(0, len(df), 6):
        avg_time = df['Total Time (M)'].iloc[i:i+6].mean()
        avg_speed = df['Segment Speed'].iloc[i:i+6].sum() / 6
        avg_times.append(avg_time)
        avg_speeds.append(avg_speed)

    averaged_data = pd.DataFrame({'Time': avg_times, 'Speed': avg_speeds})

    fig.add_trace(
        go.Scatter(x=averaged_data['Time'], y=averaged_data['Speed'],
                   mode='lines+markers',
                   marker=dict(size=4, color='#6CE5E8'),
                   name='Speed',
                   hoverinfo='text',
                   text=['Time={} min, Speed={} Km/h'.format(
                       round(time, 2), round(speed, 2)) for time, speed in zip(avg_times, avg_speeds)]
                   )
    )

    x_lims = max(avg_times) * 1.01
    y_lims = df['Segment Speed'].max() * 1.1
    
    fig.update_xaxes(range=[0, x_lims])
    fig.update_yaxes(range=[0, y_lims])
    
    average_speed = data_preparation.speed_info(df)[0]

    fig.add_shape(
        dict(
            type='line',
            x0=0,
            x1=x_lims,
            y0=average_speed,
            y1=average_speed,
            line=dict(color='#6CE5E8', width=2, dash='dash'),
            name='Average Speed Km/h',
        )
    )

    max_speed_value, ms_id = data_preparation.highest_average_speed(df)
    max_speed_time = df.iloc[ms_id]['Total Time (M)']

    max_speed_text = 'Highest Speed Obtained: Time={} min, Speed={} Km/h'.format(
        round(max_speed_time, 2), round(max_speed_value, 2))

    fig.add_trace(
        go.Scatter(x=[max_speed_time], y=[max_speed_value],
                   mode='markers',
                   marker=dict(size=12, color='#6CE5E8', symbol='diamond'),
                   hoverinfo='text',
                   text=[max_speed_text] * len(avg_times),
                   name='Highest Speed',
                   )
    )

    fig.update_layout(
        plot_bgcolor='#0B2447',
        paper_bgcolor='#0B2447',
        xaxis=dict(showgrid=False, gridcolor='#6CE5E8', title_font=dict(color='white'), tickfont=dict(color='white')),
        yaxis=dict(showgrid=False, gridcolor='#6CE5E8', title_font=dict(color='white'), tickfont=dict(color='white')),
        title_text='Time - Speed',
        title_font=dict(color='white'),
        legend=dict(
            font=dict(color='white')
        )
    )

    fig.update_traces(
        hoverlabel=dict(
            bgcolor='#123C76',
            bordercolor='#123C76',
            font=dict(size=14, color='white'),
        )
    )

    save_name = "temp/time_speed_graph.html"
    
    fig.write_html(save_name)

    return save_name


def plot_line_map(df):
    latitudes = df['Latitude'].tolist()
    longitudes = df['Longitude'].tolist()
    distances = df['Total Distance (M)'].tolist()
    altitudes = df['Altitude (M)'].tolist()
    times = df['Total Time (M)'].tolist()

    center_lat = sum(latitudes) / len(latitudes)
    center_lon = sum(longitudes) / len(longitudes)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

    route_coordinates = list(zip(latitudes, longitudes))

    folium.PolyLine(locations=route_coordinates, color='blue', weight=5, opacity=0.7).add_to(m)

    for lat, lon, dist, alt, time in zip(latitudes, longitudes, distances, altitudes, times):
        tooltip = folium.Tooltip(
            text=f"Distance: {round(dist / 1000, 2)} Km<br>Altitude: {round(alt, 1)} Metres, Time: {round(time, 1)} Minutes",
            style="font-size: 14px; background-color: #123C76; color: #FFFFFF;",
            permanent=False,
        )

        folium.CircleMarker(
            location=[lat, lon],
            radius=3,
            color='#6CE5E8',
            fill=True,
            fill_color='red',
            fill_opacity=0.7,
            tooltip=tooltip,
        ).add_to(m)
        
    dark_tile = folium.TileLayer(
        tiles='https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png',
        attr='© <a href="https://carto.com/attributions">CartoDB</a> contributors',
        name='Dark Mode',
        opacity=0.8,
    )
    dark_tile.add_to(m)
        
    map_filename = "temp/map.html"
    m.save(map_filename)
    return map_filename


def altitude_time_distance_speed_graph(df, x_choice):
    if x_choice == 'distance':
        x_axis = 'Total Distance (KM)'
        x_title = 'Distance'
        x_units = 'Km'
        x_decimals = '.2f'
    else:
        x_axis = 'Total Time (M)'
        x_title = 'Time'
        x_units = 'Mins'
        x_decimals = '.0f'
    
    fig = px.scatter(df, x=x_axis, y='Altitude (M)', color='Segment Speed', color_continuous_scale='Agsunset',
                     hover_data=[x_axis, 'Altitude (M)', 'Segment Speed'],
                     labels={x_axis: f'{x_title} ({x_units})', 'Altitude (M)': 'Altitude (m)'},
                     title=f'{x_title} - Speed - Altitude')

    if x_choice == 'distance':
        fig.update_traces(line=dict(width=4), hovertemplate='Distance: %{x:.2f} Km<br>Altitude: %{y:.1f} m<br>Segment Speed: %{marker.color:.2f} Km/h<extra></extra>')
    else:
        fig.update_traces(line=dict(width=4), hovertemplate='Time: %{x:.1f} mins<br>Altitude: %{y:.1f} m<br>Segment Speed: %{marker.color:.2f} Km/h<extra></extra>')

    fig.update_coloraxes(colorbar_title='Speed (Km/h)')

    fig.update_layout(
        plot_bgcolor='#0B2447',
        paper_bgcolor='#0B2447',
        xaxis=dict(showgrid=False, gridcolor='#2D8BBA', title_font=dict(color='white'), tickfont=dict(color='white')),
        yaxis=dict(showgrid=False, gridcolor='#2D8BBA', title_font=dict(color='white'), tickfont=dict(color='white')),
    )
    fig.update_coloraxes(
        colorbar_title_font=dict(color='white', size=14, family='Arial'),
        colorbar_tickfont=dict(color='white', size=12, family='Arial')
    )
    fig.update_layout(
        title_font=dict(color='white'),
    )
    
    fig.update_traces(
        hoverlabel=dict(
            bgcolor='#123C76',
            bordercolor='#123C76',
            font=dict(size=14, color='white'),
        )
    )
    
    fig.write_html("temp/altitude_time_distance_speed_graph.html")

    return 'temp/altitude_time_distance_speed_graph.html'


def create_custom_graph(df, x_axis, y_axis):
    if x_axis == 'distance' and y_axis == 'altitude':
        return distance_altitude_graph(df)
    
    elif x_axis == 'distance' and y_axis == 'speed':
        return distance_speed_graph(df)
    
    elif x_axis == 'time' and y_axis == 'altitude':
        return time_altitude_graph(df)
    
    elif x_axis == 'time' and y_axis == 'distance':
        return time_distance_graph(df)
    
    elif x_axis == 'time' and y_axis == 'speed':
        return time_speed_graph(df)
    
    elif x_axis == 'distance' and y_axis == 'distance':
        return None
    
    else:
        return None