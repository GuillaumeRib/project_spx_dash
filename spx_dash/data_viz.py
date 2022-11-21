####################################
# DATA VIZ - CREATE CHARTS
####################################
import plotly.express as px
import pandas as pd

color_cont = 'thermal'
col_seq = ['indianred']

def map_2d(df,color='d_avg'):
    '''
    Scatterplot GPS trace on 2D map.
    Custom feature as color
    '''
    fig = px.scatter_mapbox(df,
                            lat='latitude',
                            lon='longitude',
                            hover_name='duration',
                            hover_data=['elevation','speed','d+'],
                            mapbox_style="open-street-map",
                            zoom=9.5,
                            color=color,
                            color_continuous_scale=color_cont,
                            title='2D Map - Elevation Color',
                            #height=600
                            )
    fig.update_traces(marker=dict(size=5), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20))
    return fig


def map_3d(df,color='heart_rate'):
    '''
    3D scatterplot GPS trace.
    Custom feature as color
    '''
    fig = px.scatter_3d(df,
                        x='longitude',
                        y='latitude',
                        z='elevation',
                        hover_name='duration',
                        hover_data=['elevation','d_avg','d+'],
                        color=color,
                        color_continuous_scale=color_cont,
                        #color_continuous_midpoint=25,
                        title='3D Profile - HR color')

    fig.update_traces(marker=dict(size=3), selector=dict(mode='markers'))
    fig.update_layout(scene = {"xaxis": {"nticks": 5},
                               "zaxis": {"nticks": 10},
                               "camera_eye": {"x": -0.5, "y": 0.5, "z": 0.5},
                               "aspectratio": {"x": 1, "y": 0.7, "z": 0.25}},
                      #height=600,
                      margin=dict(l=20, r=20),

                      )
    return fig


def speed_line_dist(df,color='d_avg'):
    '''
    Line chart showing speed profile
    '''
    fig = px.line(df,
                     x='distance',
                     y='speed',
                     color_discrete_sequence=['lightgreen'],
                     hover_name='speed',
                     hover_data=['duration','speed','heart_rate','d+'],
                     title='Speed - Elevation - Heart Rate',
                     )
    fig.update_traces(marker=dict(size=3), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20, b=0),
                      height=300)
    return fig

def elev_line_dist(df):
    '''
    Line chart showing elevation profile
    '''
    fig = px.line(df,
                     x='distance',
                     y='elev_cum',
                     color_discrete_sequence=['lightblue'],
                     hover_name='elev_cum',
                     hover_data=['duration','speed','heart_rate','d+'],
                     )
    fig.update_traces(marker=dict(size=3), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20, b=0),
                      height=250)
    return fig


def hr_line_dist(df,color='d_avg'):
    '''
    Line chart showing HR profile
    '''
    fig = px.line(df,
                     x='distance',
                     y='heart_rate',
                     color_discrete_sequence=['indianred'],
                     hover_name='heart_rate',
                     hover_data=['duration','speed','heart_rate','d+'],
                     )
    fig.update_traces(marker=dict(size=3), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20, b=0),
                      height=250)
    return fig

def line_d_avg(df):
    '''
    Plot the average deniv over
    '''
    fig = px.histogram(df,
                       x='duration',
                       y='d_avg',
                       hover_name='d_avg',
                       color_discrete_sequence=col_seq,
                       title='1min Elevation gain/loss in m',
                       opacity=0.75
                       )
    fig.update_traces(marker=dict(size=3), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20))
    return fig

def histo_d_avg(df):
    '''
    Plot the average deniv over 60sec
    '''
    fig = px.histogram(df,
                       x='d_avg',
                       hover_name='d+',
                       title='1min Elevation Distribution',
                       nbins=50,
                       color_discrete_sequence=col_seq,
                       opacity=0.85
                       )
    fig.update_traces(marker=dict(size=3), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20),
                      xaxis_title="1min average elevation in m")
    return fig


def line_d_plus(df,color='d_avg'):
    '''
    Plot the cumul d+ profile
    '''
    fig = px.scatter(df,
                     x='duration',
                     y='d+',
                     color=color,
                     color_continuous_scale=color_cont,
                     hover_name='d+',
                     hover_data=['elevation','elev_cum'],
                     title='Cumul D+ m'
                     )
    fig.update_traces(marker=dict(size=3), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20))
    return fig



def scatter(df,color='heart_rate'):
    '''
    ScatterPlot Heart Rate vs d_avg
    +speed
    '''
    fig = px.scatter_3d(df,
                     x='d_avg',
                     z='heart_rate',
                     y='speed',
                     color=color,
                     color_continuous_scale=color_cont,
                     #size='speed',
                     #hover_name='elev_cum',
                     hover_data=['duration','elevation','d+'],
                     title='Heart Rate vs Speed vs Elevation'
                     )
    fig.update_traces(
        marker=dict(size=2),
        selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20),
                      height=600,
                      scene={"camera_eye": {"x": 0.5, "y": 0.5, "z": 0.5},
                             "aspectratio": {"x": 0.7, "y": 0.7, "z": 0.7}})
    return fig

def speed_violin(df):
    '''
    Plot Violin of Speed
    '''
    fig = px.violin(df,
                       y='speed',
                       title='Speed Distribution',
                       box=True,
                       color_discrete_sequence=['lightgreen']
                       )
    fig.update_traces(marker=dict(size=3), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20),
    )
    return fig

def elev_violin(df):
    '''
    Plot Violin of Elevation
    '''
    fig = px.violin(df,
                       y='d_avg',
                       title='Elevation Distribution',
                       box=True,
                       color_discrete_sequence=['lightblue']
                       )
    fig.update_traces(marker=dict(size=3), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20),
    )
    return fig

def hr_violin(df):
    '''
    Plot Violin of HR
    '''
    fig = px.violin(df,
                       y='heart_rate',
                       title='Heart Rate Distribution',
                       box=True,
                       color_discrete_sequence=['indianred']
                       )
    fig.update_traces(marker=dict(size=3), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20),
    )
    return fig
