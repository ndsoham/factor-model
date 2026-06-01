import pandas as pd
import requests
import zipfile
import os
import yfinance as yf

def fetch_stock_returns(ticker: str, start: str, end: str, cache_dir: str = "data/cache") -> pd.Series:
    """ 
    Args:
        ticker (str): stock symbol e.g. "AAPL"
        start (str): start date e.g. "2020-01-01"
        end (str): end date e.g. "2024-01-01"
        cache_dir (str, optional): Folder to store cached files. Defaults to "data/cache".

    Returns:
        pd.Series of daily returns with a DateTimeIndex, named "stock_return"
    """
    
    os.makedirs(cache_dir, exist_ok=True)
    
    cache_file = f"{cache_dir}/{ticker}_{start}_{end}.parquet"
    
    try:
        stock_return = pd.read_parquet(cache_file)["Close"]
    except FileNotFoundError:
        df = yf.download(ticker, start=start, end=end, multi_level_index=False)
        if df.empty:
            raise ValueError(f"No data found for ticker {ticker} between {start} and {end}. Check the ticker or data range")
        stock_return = df["Close"].pct_change().dropna()
        stock_return.to_frame().to_parquet(cache_file)
    
    stock_return.name = "stock_return"
    return stock_return
    

def fetch_factors(start: str, end: str, cache_dir: str = "data/cache") -> pd.DataFrame:
    """
    Args:
        start (str): start date e.g. "2026-01-01"
        end (str): end date e.g. "2026-11-31"
        cache_dir (str, optional): Folder to store cached files. Defaults to "data/cache".

    Returns:
        pd.DataFrame with DateTimeIndex and columns: Mkt-RF, SMB, HML, RF, all values converted from percentage to decimal
    """
    
    os.makedirs(cache_dir, exist_ok=True)
    
    zip_fp = f"{cache_dir}/ff_daily.zip"
    if not os.path.exists(zip_fp):
        data_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip"
        response = requests.get(data_url)
        
        with open(zip_fp, "wb") as fd:
            for chunk in response.iter_content(chunk_size=8192):
                fd.write(chunk)
    
    data_fp = f"{cache_dir}/F-F_Research_Data_Factors_daily.csv"
    
    if not os.path.exists(data_fp):
        with zipfile.ZipFile(zip_fp) as data_zip:
            data_zip.extractall(f"{cache_dir}")
            
    cache_fp = f"{cache_dir}/ff_factors_{start}_{end}.parquet"
    
    if not os.path.exists(cache_fp):
        df = pd.read_csv(data_fp, skiprows=4, skipfooter=1, index_col=0, engine="python")
        df.index = pd.to_datetime(df.index, format="%Y%m%d")
        df = df/100
        df = df.loc[start:end, :]
        df.to_parquet(cache_fp)
        return df
    else:
        return pd.read_parquet(cache_fp)