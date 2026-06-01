from data.fetcher import fetch_factors, fetch_stock_returns
from model.regression import run_regression

start_date = "2021-11-09"
end_date = "2026-06-01"
ticker = "AAPL"

stock_returns = fetch_stock_returns(ticker, start_date, end_date)
factors = fetch_factors(start_date, end_date)
results = run_regression(stock_returns, factors)
print(results.params)