from data.fetcher import fetch_factors, fetch_stock_returns
from model.regression import run_regression
from metrics.performance import compute_metrics
from dashboard.app import plot_dashboard
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Fama 3 Factor Model")
    
    parser.add_argument("--ticker", type=str, default="AAPL")
    parser.add_argument("--start", type=str, default="2021-11-9")
    parser.add_argument("--end", type=str, default="2026-05-28")
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    stock_returns = fetch_stock_returns(args.ticker, args.start, args.end)
    factors = fetch_factors(args.start, args.end)
    results, aligned = run_regression(stock_returns, factors)
    metrics = compute_metrics(results)

    plot_dashboard(results, metrics, aligned, args.ticker)
    
if __name__ == "__main__":
    main()





