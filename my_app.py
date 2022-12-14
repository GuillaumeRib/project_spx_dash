####################################
# IMPORTS
####################################

import pandas as pd
import datetime

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from spx_dash import get_data
from spx_dash import data_viz


####################################
# Load data & dfs
####################################
df = get_data.load_wiki_cons('spx_dash/wiki_cons.csv')
weights = get_data.load_IVV_weight()
df = get_data.join_dfs(df,weights)
returns_df = get_data.get_returns()

stock_df = get_data.get_stock_perf(returns_df,df)
sector_df, ind_df, sector_cum_perf = get_data.get_sector_perf(returns_df,df)




####################################
# INIT APP
####################################
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX, dbc_css],
                meta_tags=[{'name':'viewport',
                            'content':'width=device-width,initial-scale=1.0'}]
                )
server=app.server



####################################
# SELECT TEMPLATE for the APP
####################################
# loads the template and sets it as the default
load_figure_template("lux")


####################################
# FILL Template layout
####################################

title = html.H1(children="S&P 500 Monitor",
                className=('text-center mb-4'))
as_of = html.H5(children=f'last update: {returns_df.index[-1].year}-{returns_df.index[-1].month}-{returns_df.index[-1].day}',
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
        dbc.Col(as_of,width=12,class_name=('text-center mt-4'))
    ]),

    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=data_viz.tree(stock_df,'YTD')),
            xs=12,sm=12,md=12,lg=12,xl=6,xxl=6,class_name=('mt-4')),
        dbc.Col(
            dcc.Graph(figure=data_viz.bar_sec(sector_df)),
            xs=12,sm=12,md=12,lg=12,xl=6,xxl=6,class_name=('mt-4')),
    ]),

    dbc.Row([
            dbc.Col(
                dcc.Graph(figure=data_viz.line_sector(sector_cum_perf)),
                xs=12,sm=12,md=12,lg=12,xl=12,xxl=12,class_name=('mt-4')),
    ]),


    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=data_viz.scat_stock(stock_df)),
            xs=12,sm=12,md=12,lg=12,xl=12,xxl=12,class_name=('mt-4')),
        dbc.Col(
            dcc.Graph(figure=data_viz.scat_ind(stock_df,'YTD')),
            xs=12,sm=12,md=12,lg=12,xl=12,xxl=12,class_name=('mt-4')),
    ]),




],
                           fluid=True,
                           className="dbc")


####################################
# RUN the app
####################################
if __name__ == '__main__':
    server=app.server
    app.run_server(debug=True)
