import plotly.graph_objects as go
from PIL import Image

def create_time_distance_graph(df):
    image_path = "images/bg.jpg"
    img = Image.open(image_path)
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['Total Time (M)'], y=df['Total Distance (M)'],
                   line=dict(width=3, color='red'),
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
                opacity=0.8,
                layer="below")
    )

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)

    fig.update_xaxes(title_text='Time (minutes)')
    fig.update_yaxes(title_text='Distance (Km)')

    fig.update_layout(title_text='Distance Over Time')

    return fig.show()

def create_altitude_distance_graph(df):
    image_path = "images/bg.jpg"
    img = Image.open(image_path)
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['Total Distance (M)'], y=df['Altitude (M)'],
                   line=dict(width=3, color='red'),
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
                opacity=0.8,
                layer="below")
    )

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)

    fig.update_xaxes(title_text='Distance (Km)')
    fig.update_yaxes(title_text='Altitude (M)')

    fig.update_layout(title_text='Altitude over Distance')

    return fig.show()