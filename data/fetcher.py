import pandas as pd
import requests
import zipfile
import io
import os

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
            for chunk in response.iter_content():
                fd.write(chunk)
    
    data_fp = f"{cache_dir}/F-F_Research_Data_Factors_daily.csv"
    
    if not os.path.exists(data_fp):
        with zipfile.ZipFile(zip_fp) as data_zip:
            data_zip.extractall(f"{cache_dir}")
            
    df = pd.read_csv(data_fp, skiprows=4, skipfooter=1, index_col=0, parse_dates=True, date_format="%Y%m%d")
