import plotly.graph_objects as go
from PIL import Image

def create_time_distance_graph(df):
    image_path = "images/bg.jpg"
    img = Image.open(image_path)
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['Total Time (M)'], y=df['Total Distance (M)'],
                   line=dict(width=5, color='red'),
                   hovertext=['Time={} min, Distance={} Km'.format(round(time, 1), round(distance / 1000, 2))
                              for i, (time, distance) in enumerate(zip(df['Total Time (M)'], df['Total Distance (M)']))],
                   mode='lines+markers',
                   )
    )

    # Add images
    fig.add_layout_image(
            dict(
                source=img,
                xref="x",
                yref="y",
                x=0,
                y=90000,
                sizex=250,
                sizey=90000,
                sizing="stretch",
                opacity=0.8,
                layer="below")
    )

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)

    fig.update_xaxes(title_text='Time (minutes)')
    fig.update_yaxes(title_text='Distance (Km)')

    fig.update_layout(title_text='Distance Over Time')

    return fig.show()