####################################
# MAIN PAGE
####################################
import plotly.express as px
import pandas as pd
from data_viz import sun
import get_data




if __name__ == '__main__':
    print('main')
    csv_path = 'spx.csv'
    df = get_data.get_spx_cons()
    get_data.get_prices(df,csv_path)
