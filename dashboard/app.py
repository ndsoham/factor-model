from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

def plot_dashboard(results, metrics: dict, aligned: pd.DataFrame, ticker: str) -> None:
    """
    Args:
        results (_type_): statsmodels RegressionResults object
        metrics (dict): dict from compute_metrics
        aligned (pd.DataFrame): aligned dataframe or market and stock returns
        ticker (str): ticker for stock, used for plot title
    """
    
    figure = make_subplots(
        rows=3, cols=1, 
        subplot_titles=("Actual vs Fitted Returns", "Rolling 60-day Beta", "Metrics"),
        specs=[
        [{"type" : "xy"}],
        [{"type" : "xy"}],
        [{"type" : "table"}]
    ])
    
    figure.update_layout(title_text=f"{ticker} Fama-French 3-Factor Model", title_x=0.5)
    
    ### Panel 1
    X = results.fittedvalues.index
    y_pred = results.fittedvalues.values
    y_true = results.model.endog
    
    figure.add_trace(
        go.Scatter(x=X, y=y_pred, mode="markers", name="Predicted"), row=1, col=1
    )
    
    figure.add_trace(
        go.Scatter(x=X, y=y_true, name="Actual"), row=1, col=1
    )
    
    figure.update_xaxes(title_text="Date", row=1, col=1)
    figure.update_yaxes(title_text="Returns", row=1, col=1)
    
    ### Panel 2
    # beta = cov(stock, mkt) / var(mkt)
    rolling_cov = aligned.loc[:, "excess"].rolling(60).cov(aligned.loc[:, "Mkt-RF"])
    rolling_var = aligned.loc[:, "Mkt-RF"].rolling(60).var()
    rolling_beta = rolling_cov / rolling_var
    
    X = aligned.index[:-59]
    y = rolling_beta
    
    figure.add_trace(
        go.Scatter(x=X, y=y, name="Beta"), row=2, col=1
    )
    figure.update_xaxes(title_text="Date", row=2, col=1)
    figure.update_yaxes(title_text="Beta", row=2, col=1)
    
    ### Panel 3
    metric_names = list(metrics.keys())
    metric_values = [v if k not in ["t_stats", "p_values"] else list(v.values()) for k, v in metrics.items()]
    
    figure.add_trace(
        go.Table(header=dict(values=["Metric", "Value"]), 
                 cells=dict(values=[metric_names, metric_values])), row=3, col=1
    )
    
    
    figure.show()
    