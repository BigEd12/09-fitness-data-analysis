import pandas as pd
import plotly.graph_objects as go
from PIL import Image

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

def create_altitude_distance_graph(df):
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

    return fig.show()



def create_speed_distance_graph(df):
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