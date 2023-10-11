import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import folium

def create_time_distance_graph(df):
    image_path = "images/bg.jpg"
    img = Image.open(image_path)
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['Total Time (M)'], y=df['Total Distance (M)'],
                   line=dict(width=1, color='red'),
                   hovertext=['Time={} min, Distance={} Km'.format(round(time, 1), round(distance / 1000, 2))
                              for i, (time, distance) in enumerate(zip(df['Total Time (M)'], df['Total Distance (M)']))],
                   mode='lines+markers',
                   )
    )
    
    x_lims = df.iloc[-1]['Total Time (M)'] * 1.1
    y_lims = df.iloc[-1]['Total Distance (M)'] * 1.1
    
    fig.add_layout_image(
            dict(
                source=img,
                xref="x",
                yref="y",
                x=0,
                y=y_lims,
                sizex=x_lims,
                sizey=y_lims,
                sizing="stretch",
                opacity=0.7,
                layer="below")
    )

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)

    fig.update_xaxes(title_text='Time (minutes)', range=[0, x_lims])
    fig.update_yaxes(title_text='Distance (Km)', range=[0, y_lims])

    fig.update_layout(title_text='Distance Over Time')

    return fig.show()

def altitude_distance_graph(df):
    image_path = "images/bg.jpg"
    img = Image.open(image_path)
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['Total Distance (M)'], y=df['Altitude (M)'],
                   line=dict(width=1, color='red'),
                   hovertext=['Distance={} Km, Altitude={} M'.format(round(distance / 1000, 2, ), round(altitude, 2))
                              for i, (distance, altitude) in enumerate(zip(df['Total Distance (M)'], df['Altitude (M)']))],
                   mode='lines+markers',
                   )
    )
    
    x_lims = df.iloc[-1]['Total Distance (M)'] * 1.1
    y_lims = df['Altitude (M)'].max() * 1.1
    
    fig.add_layout_image(
            dict(
                source=img,
                xref="x",
                yref="y",
                x=0,
                y=y_lims,
                sizex=x_lims,
                sizey=y_lims,
                sizing="stretch",
                opacity=0.7,
                layer="below")
    )

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)

    fig.update_xaxes(title_text='Distance (Km)', range=[0, x_lims])
    fig.update_yaxes(title_text='Altitude (M)', range=[0, y_lims])

    fig.update_layout(title_text='Altitude over Distance')
    
    fig.write_html("temp/altitude_distance_chart.html")

    return 'altitude_distance_chart.html'


def altitude_time_graph(df):
    image_path = "images/bg.jpg"
    img = Image.open(image_path)
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['Total Time (M)'], y=df['Altitude (M)'],
                   line=dict(width=1, color='red'),
                   hovertext=['Time={} min, Altitude={} M'.format(round(time, 2), round(altitude, 2))
                              for time, altitude in zip(df['Total Time (M)'], df['Altitude (M)'])],
                   mode='lines+markers',
                   )
    )
    
    x_lims = df.iloc[-1]['Total Time (M)'] * 1.1
    y_lims = df['Altitude (M)'].max() * 1.1
    
    fig.add_layout_image(
            dict(
                source=img,
                xref="x",
                yref="y",
                x=0,
                y=y_lims,
                sizex=x_lims,
                sizey=y_lims,
                sizing="stretch",
                opacity=0.7,
                layer="below")
    )

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)

    fig.update_xaxes(title_text='Time (min)', range=[0, x_lims])
    fig.update_yaxes(title_text='Altitude (M)', range=[0, y_lims])

    fig.update_layout(title_text='Altitude over Time')

    return fig.show()



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
                   marker=dict(size=4, color='#E4F1FF'),
                   name='Speed',
                   hovertext=['Distance={} Km, Speed={} Km/h'.format(
                       round(distance / 1000, 2), round(speed, 2)) for distance, speed in zip(avg_distances, avg_speeds)]
                   )
    )

    x_lims = df['Total Distance (M)'].max() * 1.01
    y_lims = df['Segment Speed'].max() * 1.1

    fig.update_layout(
        xaxis_showgrid=False, yaxis_showgrid=False,
        xaxis_title='Distance (Km)', yaxis_title='Speed (Km/h)',
        title_text='Speed over Distance',
        plot_bgcolor='#132043',
        paper_bgcolor='#E5E5E5'
    )

    fig.update_xaxes(range=[0, x_lims])
    fig.update_yaxes(range=[0, y_lims])
    
    fig.add_trace(go.Scatter(x=averaged_data['Distance'], y=averaged_data['Speed'], fill='tozeroy', fillcolor='#E4F1FF'))
    
    
    fig.add_shape(
        dict(
            type='line',
            x0=0,
            x1=x_lims,
            y0=sum(avg_speeds) / len(avg_speeds),  # Average speed
            y1=sum(avg_speeds) / len(avg_speeds),
            line=dict(color='red', width=2, dash='dash'),
            name='Average Speed Km/h',
        )
    )
    
    
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='red', width=2, dash='dash'), name='Average Speed Km/h', showlegend=True))

    fig.add_trace(
        go.Scatter(x=[df.iloc[df['Segment Speed'].idxmax()]['Total Distance (M)']], y=[df['Segment Speed'].max()],
                   mode='markers',
                   marker=dict(size=12, color='#E4F1FF'),
                   hovertext=['Highest Speed Obtained: Distance={} Km, Speed={} Km/h'.format(
                       round(df.iloc[df['Segment Speed'].idxmax()]['Total Distance (M)'] / 1000, 2), round(df['Segment Speed'].max(), 2)) for distance, speed in zip(avg_distances, avg_speeds)],
                   name='Highest Speed',
                   )
    )

    return fig.show()


def time_speed_graph(df):
    fig = go.Figure()

    window_size = 6
    num_windows = len(df) // window_size

    avg_times = []
    avg_speeds = []

    for i in range(num_windows):
        start_idx = i * window_size
        end_idx = (i + 1) * window_size

        avg_time = df['Total Time (M)'].iloc[start_idx:end_idx].mean()
        avg_speed = df['Segment Speed'].iloc[start_idx:end_idx].sum() / window_size

        avg_times.append(avg_time)
        avg_speeds.append(avg_speed)

    averaged_data = pd.DataFrame({'Time': avg_times, 'Speed': avg_speeds})

    fig.add_trace(
        go.Scatter(x=averaged_data['Time'], y=averaged_data['Speed'],  # Use 'Time' instead of 'Distance'
                   mode='lines+markers',
                   marker=dict(size=4, color='#E4F1FF'),
                   name='Speed',
                   hovertext=['Time={} min, Speed={} Km/h'.format(
                       round(time, 2), round(speed, 2)) for time, speed in zip(avg_times, avg_speeds)]
                   )
    )

    x_lims = max(avg_times) * 1.01  # Adjust x-axis limit for time
    y_lims = df['Segment Speed'].max() * 1.1

    fig.update_layout(
        xaxis_showgrid=False, yaxis_showgrid=False,
        xaxis_title='Time (min)', yaxis_title='Speed (Km/h)',
        title_text='Speed over Time',  # Update the title
        plot_bgcolor='#132043',
        paper_bgcolor='#E5E5E5'
    )

    fig.update_xaxes(range=[0, x_lims])
    fig.update_yaxes(range=[0, y_lims])
    
    fig.add_trace(go.Scatter(x=averaged_data['Time'], y=averaged_data['Speed'], fill='tozeroy', fillcolor='#E4F1FF'))
    
    fig.add_shape(
        dict(
            type='line',
            x0=0,
            x1=x_lims,
            y0=sum(avg_speeds) / len(avg_speeds),  # Average speed
            y1=sum(avg_speeds) / len(avg_speeds),
            line=dict(color='red', width=2, dash='dash'),
            name='Average Speed Km/h',
        )
    )
    
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='red', width=2, dash='dash'), name='Average Speed Km/h', showlegend=True))

    fig.add_trace(
        go.Scatter(x=[df.iloc[df['Segment Speed'].idxmax()]['Total Time (M)']], y=[df['Segment Speed'].max()],
                   mode='markers',
                   marker=dict(size=12, color='#E4F1FF'),
                   hovertext=['Highest Speed Obtained: Time={} min, Speed={} Km/h'.format(
                       round(df.iloc[df['Segment Speed'].idxmax()]['Total Time (M)'], 2), round(df['Segment Speed'].max(), 2)) for time, speed in zip(avg_times, avg_speeds)],
                   name='Highest Speed',
                   )
    )

    return fig.show()


def plot_line_map(df):
    latitudes = df['Latitude'].tolist()
    longitudes = df['Longitude'].tolist()
    distances = df['Total Distance (M)'].tolist()
    altitudes = df['Altitude (M)'].tolist()
    times = df['Total Time (M)'].tolist()

    center_lat = sum(latitudes) / len(latitudes)
    center_lon = sum(longitudes) / len(longitudes)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

    route_coordinates = list(zip(latitudes, longitudes))

    folium.PolyLine(locations=route_coordinates, color='blue', weight=5, opacity=0.7).add_to(m)

    for lat, lon, dist, alt, time in zip(latitudes, longitudes, distances, altitudes, times):
        folium.CircleMarker(
            location=[lat, lon],
            radius=3,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.7,
            tooltip=f"Distance: {round(dist / 1000, 2)} Km, Altitude: {round(alt, 1)} Metres, Time: {round(time, 1)} Minutes"
        ).add_to(m)
        
    map_filename = "temp/map.html"
    m.save(map_filename)
    return map_filename


def altitude_time_speed_graph(df):
    fig = px.scatter(df, x='Total Time (M)', y='Altitude (M)', color='Segment Speed', color_continuous_scale='Viridis',
                     hover_data=['Total Time (M)', 'Altitude (M)', 'Segment Speed'],
                     labels={'Total Time (M)': 'Time (mins)', 'Altitude (M)': 'Altitude (m)'},
                     title='Time by Altitude and Speed')

    fig.add_trace(px.line(df, x='Total Time (M)', y='Altitude (M)', color='Altitude (M)').data[0])

    fig.update_traces(line=dict(width=4), hovertemplate='Time: %{x:.1f} mins<br>Altitude: %{y:.1f} m<br>Segment Speed: %{marker.color:.2f} Km/h<extra></extra>')
    fig.update_coloraxes(colorbar_title='Speed (m/s)')

    return fig.show()


def altitude_distance_speed_graph(df):
    fig = px.scatter(df, x='Total Distance (KM)', y='Altitude (M)', color='Segment Speed', color_continuous_scale='Agsunset',
                     hover_data=[('Total Distance (KM)'), 'Altitude (M)', 'Segment Speed'],
                     labels={'Total Distance (KM)': 'Distance (Km)', 'Altitude (M)': 'Altitude (m)'},
                     title='Distance - Speed - Altitude')

    fig.add_trace(px.line(df, x='Total Distance (KM)', y='Altitude (M)', color='Altitude (M)').data[0])

    fig.update_traces(line=dict(width=4), hovertemplate='Distance: %{x:.2f} Km<br>Altitude: %{y:.1f} m<br>Segment Speed: %{marker.color:.2f} Km/h<extra></extra>')
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
            font=dict(size=24, color='white'),
        )
    )

    fig.write_html("temp/altitude_distance_speed_graph.html")

    return 'altitude_distance_speed_graph.html'