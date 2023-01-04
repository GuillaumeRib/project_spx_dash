import pandas as pd
import numpy as np
import yfinance as yf

####################################
# GET FUNCTIONS
####################################

# GETTING S&P 500 constituents from Wikipedia - Save to csv
def get_spx_cons(csv_path):
    '''
    Extract S&P 500 companies from wikipedia and store tickers and Sectors / Industries as df
    Then store as csv.
    '''
    URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    df = pd.read_html(URL)[0]
    df['Symbol'] = df['Symbol'].str.replace('.','-')
    df = df.drop(['SEC filings','Headquarters Location','Date first added','CIK','Founded'],axis=1)
    df = df.sort_values(by=['GICS Sector','GICS Sub-Industry'])
    df = df.set_index('Symbol')
    df.dropna(inplace=True)
    return df.to_csv(csv_path)

# GETTING S&P prices from yfinance - Save to csv
def get_prices(df,csv_path):
    '''
    Dowload prices from yfinance from a list of tickers. returns df of prices written to a csv
    '''
    tickers_list = df.index.tolist()
    start= '2010-12-31'
    prices_df = yf.download(tickers_list, start=start,interval='1d',)
    return prices_df['Adj Close'].to_csv(csv_path)


####################################
# LOAD FUNCTIONS
####################################

# load S&P 500 weights from IVV ETF stored in csv
def load_IVV_weight():
    '''
    Load weights from IVV Holdings csv => df_IVV
    '''
    df_IVV = pd.read_csv('spx_dash/IVV_holdings.csv',skiprows=8,header=1)
    df_IVV = df_IVV[df_IVV['Asset Class']=='Equity']
    df_IVV = df_IVV[['Ticker','Name','Sector','Asset Class','Weight (%)']]
    df_IVV = df_IVV.set_index('Ticker')
    df_IVV.index = df_IVV.index.str.replace('BRKB','BRK-B')
    df_IVV.index = df_IVV.index.str.replace('BFB','BF-B')
    df_IVV['Weight (%)'] = df_IVV['Weight (%)']/100
    return df_IVV

# load S&P 500 weights from IVV ETF stored in csv
def load_wiki_cons(csv_path):
    '''
    Load tickers, sectors, industries etc. from wiki csv file
    => df
    '''
    df = pd.read_csv(csv_path)
    df = df.set_index('Symbol')
    return df

####################################
# COMPUTE FUNCTIONS
####################################

# Computing Monthly and Daily returns
def get_returns():
    '''
    Load prices from csv and compute monthly returns.
    output returns_df
    '''
    file = 'spx_dash/spx.csv'
    prices_csv = pd.read_csv(file).set_index('Date')
    prices_csv.index = pd.to_datetime(prices_csv.index)
    # fwd fill last prices to missing daily prices (non-trading). resample as Monthly.
    mth_prices_csv = prices_csv.asfreq('D').ffill().asfreq('M').ffill()
    returns_df = mth_prices_csv.pct_change()
    daily_prices_csv = prices_csv.asfreq('D').ffill()
    returns_daily_df = daily_prices_csv.pct_change()
    return returns_df, returns_daily_df


# Computing returns - 1M, 3M, and YTD
def get_returns_period(returns_df,df):
    '''
    Add monthly returns stats to original df. Output df with returns data
    '''
    df_ret_summ = pd.DataFrame((returns_df[-1:]+1).prod()-1,columns=['1M'])
    df_ret_summ['3M'] = (returns_df[-3:]+1).prod()-1
    df_ret_summ['YTD'] = (returns_df['2022']+1).prod()-1
    df_ret_summ.index.rename('Symbol',inplace=True)
    df = df.join(df_ret_summ)
    return df


# Computing sector cumulative performance for line chart
def get_sector_cum_returns(returns_daily_df,df,period='2022'):
    '''
    from df of monthly returns for each stocks compute sector cum performance vs EW
    '''
    sector_cum_perf_df = returns_daily_df['2022'].T
    sector_cum_perf_df.index.rename('Symbol',inplace=True)
    sector_cum_perf_df = df.join(sector_cum_perf_df)
    sector_cum_perf_df = sector_cum_perf_df.drop(columns='Weight')
    sector_cum_perf_df = sector_cum_perf_df.groupby('Sector').mean().T
    sector_cum_perf_df = (sector_cum_perf_df+1).cumprod()*100
    sector_cum_perf_df.loc[pd.to_datetime('2021-12-31')]= 100
    sector_cum_perf_df = sector_cum_perf_df.sort_index()
    return sector_cum_perf_df

####################################
# FEATURE ENGINEERING
####################################
def join_dfs(df,df_IVV):
    df = df.join(df_IVV['Weight (%)'])
    df.sort_values(by='Weight (%)',inplace=True,ascending=False)
    df = df.rename(columns={'GICS Sector':'Sector','GICS Sub-Industry':'Sub-Industry','Weight (%)':'Weight'})
    return df
