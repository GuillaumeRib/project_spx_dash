####################################
# DATA VIZ - CREATE CHARTS
####################################
import plotly.express as px
import pandas as pd

def sun(df,period='1M'):
    '''
    Plot a sunburst of S&P Sector industry and stocks by Size=weight, Color=Perf
    '''
    color_cont=['red','white','green']
    fig = px.sunburst(df,
                      path= ['Sector', 'Sub-Industry','Security'], #key arg for plotly to create hierarchy based on tidy data
                      values='Weight',
                      color=period,
                      color_continuous_scale=color_cont,
                      color_continuous_midpoint=0,
                      range_color=[-0.5,0.5],
                      #hover_name=period,
                      hover_data={period:':.4f'}
                 )
    fig.update_traces(marker=dict(size=5), selector=dict(mode='markers')
                     )
    fig.update_layout(margin=dict(l=20, r=20),
                      title=f'S&P 500 Performance Sunburst Overview - {period}',
                     height=800)
    return fig
