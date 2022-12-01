import pandas as pd
import yfinance as yf

####################################
# GETTING S&P 500 constituents from Wikipedia
####################################

def get_spx_cons():
    '''
    Extract S&P 500 companies from wikipedia and store tickers and Sectors / Industries as df
    '''

    URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    df = pd.read_html(URL)[0]
    df['Symbol'] = df['Symbol'].str.replace('.','-')
    df = df.drop(['SEC filings','Headquarters Location','Date first added','CIK','Founded'],axis=1)
    df = df.sort_values(by=['GICS Sector','GICS Sub-Industry'])
    df = df.set_index('Symbol')
    return df

####################################
# GETTING S&P 500 weights from IVV ETF stored in csv
####################################
def get_IVV_weight():
    df_IVV = pd.read_csv('spx_dash/IVV_holdings.csv',skiprows=8,header=1)
    df_IVV = df_IVV[df_IVV['Asset Class']=='Equity']
    df_IVV = df_IVV[['Ticker','Name','Sector','Asset Class','Weight (%)']]
    df_IVV = df_IVV.set_index('Ticker')
    df_IVV.index = df_IVV.index.str.replace('BRKB','BRK-B')
    df_IVV.index = df_IVV.index.str.replace('BFB','BF-B')
    return df_IVV

####################################
# GETTING S&P prices from yfinance - Loading from csv
####################################

def get_prices(df,csv_path):
    '''
    Dowload prices from yfinance from a list of tickers. returns df of prices written to a csv
    '''
    tickers_list = df.index.tolist()
    start= '2010-12-31'
    prices_df = yf.download(tickers_list, start=start,interval='1d',)
    return prices_df['Adj Close'].to_csv(csv_path)

def load_prices_get_returns():
    '''
    Load prices from csv and compute daily returns.
    output returns_df
    '''
    file = 'spx_dash/spx.csv'
    prices_csv = pd.read_csv(file).set_index('Date')
    prices_csv.index = pd.to_datetime(prices_csv.index)
    returns_df = prices_csv.pct_change()
    #returns_df = returns_df.iloc[:-1] if need to delete last day (current day)
    return returns_df

def get_returns_period(returns_df,df):
    '''
    Join returns stats with original df. Output df with returns data
    '''
    df_ret_summ = pd.DataFrame((returns_df[-23:-1]+1).prod()-1,columns=['1M'])
    df_ret_summ['3M'] = (returns_df[-67:-1]+1).prod()-1
    df_ret_summ['YTD'] = (returns_df['2022'][:-1]+1).prod()-1
    df = df.join(df_ret_summ)
    return df



####################################
# FEATURE ENGINEERING
####################################
def join_dfs(df,df_IVV):
    df = df.join(df_IVV['Weight (%)'])
    df.sort_values(by='Weight (%)',inplace=True,ascending=False)
    df = df.rename(columns={'GICS Sector':'Sector','GICS Sub-Industry':'Sub-Industry','Weight (%)':'Weight'})
    return df
