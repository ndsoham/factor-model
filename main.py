from data.fetcher import fetch_factors, fetch_stock_returns
from model.regression import run_regression
from metrics.performance import compute_metrics
from dashboard.app import plot_dashboard

start_date = "2021-11-9"
end_date = "2026-06-01"
ticker = "AAPL"

stock_returns = fetch_stock_returns(ticker, start_date, end_date)
factors = fetch_factors(start_date, end_date)
results, aligned = run_regression(stock_returns, factors)
metrics = compute_metrics(results)
plot_dashboard(results, metrics, aligned, ticker)
