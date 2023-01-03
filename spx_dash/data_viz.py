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
                      #range_color=[-0.5,0.5],
                      #hover_name=period,
                      hover_data={period:':.4f'}
                 )
    fig.update_traces(marker=dict(size=5), selector=dict(mode='markers')
                     )
    fig.update_layout(margin=dict(l=20, r=20),
                      title=f'S&P 500 | Composition and Performance Highlight - {period}',
                     height=600)
    return fig

def violin_sec(df,period='1M'):
    '''
    Plot Violin Dispersion plot of S&P sector for period performance
    '''
    df = df
    fig = px.violin(df,
                    x='Sector',
                    y=period,
                    color='Sector',
                    hover_name='Security',
                    box=True,
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    #range_y=(-1,1.5)
                    )


    fig.update_layout(margin=dict(l=20, r=20),
                      title=f'Dispersion By Sector - {period}',
                      showlegend=False,
                      height=600

                      )
    return fig


def scat_ind(df,period='1M'):
    '''

    '''
    df = df.groupby(by=['Sub-Industry','Sector',],as_index=False).mean()
    df= df.sort_values(by=period,ascending=False)

    fig = px.scatter(df,
                    x='Sub-Industry',
                    y=period,
                    color='Sector',
                    hover_name='Sub-Industry',
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    hover_data={period:':.4f'}
                    #size='Weight',
                )
    fig.update_traces(marker=dict(size=8), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20),
                      title=f'Sub-Industry Top/Worst Performers by Sector - {period}',
                     height=800,
                     )
    return fig


def tree(df,period='1M'):
    '''

    '''
    color_cont=['red','white','green']
    fig = px.treemap(df,
                     path= ['Sector','Sub-Industry','Security'], #key arg for plotly to create hierarchy based on tidy data
                     values='Weight',
                     color=period,
                     color_continuous_scale=color_cont,
                     color_continuous_midpoint=0,
                     #range_color=[-0.5,0.5],
                     hover_data={period:':.4f'},
                     title=''
                 )
    fig.update_traces(marker=dict(size=5), selector=dict(mode='markers'))
    fig.update_layout(margin=dict(l=20, r=20),
                     height=600)
    return fig

def bar_sec(df,period='1M'):
    '''

    '''
    df = df.groupby(by='Sector').mean()
    df= df.sort_values(by=period,ascending=False)

    fig = px.bar(df,
                 x=df.index,
                 y=[period,'YTD'],
                 color_discrete_sequence=['indianred','grey'],
                 barmode='group',

                )

    fig.update_layout(margin=dict(l=20, r=20),
                      title='EW Sector Returns - 1M vs YTD',
                     height=600,)
    return fig


def scat_stock(df):
    '''

    '''
    fig = px.scatter(df,
                     x='YTD',
                     y='1M',
                     color='Sector',
                     size='Weight',
                     hover_name='Security',
                     size_max=40,
                     color_discrete_sequence=px.colors.qualitative.Plotly,
                     hover_data={'1M':':.4f','YTD':':.4f'},
                     title='Stock Return 1M vs YTD'

                )
    fig.update_traces(marker=dict(
        line=dict(
        width=0.5,
        color='DarkSlateGrey')
    ))
    fig.update_layout(margin=dict(l=20, r=20),
                     height=600,
                    )
    return fig
