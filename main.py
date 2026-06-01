from data.fetcher import fetch_factors, fetch_stock_returns

print(fetch_stock_returns("AAPL", "2026-01-01", "2026-03-01"))
print(fetch_factors("2026-01-01", "2026-03-01").index)