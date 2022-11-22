####################################
# MAIN PAGE
####################################
import plotly.express as px
import pandas as pd
from data_viz import sun
import get_data




if __name__ == '__main__':
    print('main')

    df = get_data.get_spx_cons()
    df_IVV = get_data.get_IVV_weight()
    df = get_data.join_dfs(df,df_IVV)
    returns_df = get_data.load_prices_get_returns( )
    df = get_data.get_returns_period(returns_df,df)
    sun(df,'YTD')
