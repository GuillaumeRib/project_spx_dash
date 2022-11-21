####################################
# IMPORTS
####################################

import pandas as pd

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from gpx_viewer.interface import get_data
from gpx_viewer.interface import data_viz


###################################
# CONVERT GPX to Dataframe
####################################
test_path = 'gpx_viewer/data/Ambert_Col_des_Supeyres.gpx'
test_fit_path = 'gpx_viewer/data/8685365728.fit'

# To load GPX files
#df = get_data.get_gpx(gpx_path=test_path)
#df = get_data.data_feat_eng(df)

# To load FIT files
fit_df = get_data.get_dataframes(test_fit_path)
df = get_data.data_feat_eng_FIT(fit_df)

####################################
# INIT APP
####################################
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css],
                meta_tags=[{'name':'viewport',
                            'content':'width=device-width,initial-scale=1.0'}]
                )
server=app.server

###################################
# SELECT TEMPLATE for the APP
####################################
# loads the template and sets it as the default
load_figure_template("darkly")


###################################
# IMPORT Charts
####################################
map_2d = dcc.Graph(figure=data_viz.map_2d(df))
map_3d = dcc.Graph(figure=data_viz.map_3d(df))
#d_avg = dcc.Graph(figure=data_viz.line_d_avg(df))
#histo = dcc.Graph(figure=data_viz.histo_d_avg(df))
#d_plus = dcc.Graph(figure=data_viz.line_d_plus(df))
scatter = dcc.Graph(figure=data_viz.scatter(df))
elev_line_dist = dcc.Graph(figure=data_viz.elev_line_dist(df))
speed_line_dist = dcc.Graph(figure=data_viz.speed_line_dist(df))
hr_line_dist = dcc.Graph(figure=data_viz.hr_line_dist(df))
speed_violin = dcc.Graph(figure=data_viz.speed_violin(df))
elev_violin = dcc.Graph(figure=data_viz.elev_violin(df))
hr_violin = dcc.Graph(figure=data_viz.hr_violin(df))


####################################
# FILL Template layout
####################################

title = html.H1(children="GPS Fit Data Visualization",
                className=('text-center mb-4'))


# Max 12 col available - choose size for screen size
xs=12
sm=12
md=12
lg=12
xl=6
xxl=6


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(title,width=12,class_name=('mt-4'))
    ]),
    dbc.Row([
        dbc.Col(html.H4(children=f'{df.distance.max().round(2)} km'),
            class_name=('text-info',
            "text-center",
            'mb+4'),
            width=3),
        dbc.Col(html.H4(children=f'{df.speed.mean().round(2)} km/h'),
            class_name=('text-info',
            "text-center",
            'mb+4'),
            width=3),
        dbc.Col(html.H4(children=f'{df.heart_rate.mean().round(2)} bpm'),
            class_name=('text-info',
            "text-center",
            'mb+4'),
            width=3),
        dbc.Col(html.H4(children=f"D+ {df['d+'].max().round(2)} m"),
            class_name=('text-info',
            "text-center",
            'mb+4'),
            width=3),
        ]),
    dbc.Row([
        dbc.Col(map_2d,
            xs=xs,sm=sm,md=md,lg=lg,xl=xl,xxl=xxl),
        dbc.Col(map_3d,
            xs=xs,sm=sm,md=md,lg=lg,xl=xl,xxl=xxl),
        ],class_name='mt-4'),
    dbc.Row([
        speed_line_dist,
        elev_line_dist,
        hr_line_dist,
    ],class_name='mt-4'),
    dbc.Row([
        dbc.Col(speed_violin,
                xs=4,sm=4,md=4,lg=4,xl=4,xxl=4),
        dbc.Col(elev_violin,
                xs=4,sm=4,md=4,lg=4,xl=4,xxl=4),
        dbc.Col(hr_violin,
                xs=4,sm=4,md=4,lg=4,xl=4,xxl=4),
    ],class_name='mt-4'),
    dbc.Row([
        dbc.Col(scatter,
                width=12),
    ],class_name='mt-4',justify=True)],
                        fluid=True,
                        className="dbc")


####################################
# RUN the app
####################################
if __name__ == '__main__':
    server=app.server
    app.run_server(debug=True)
