from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plot_dashboard(results, metrics: dict, ticker: str) -> None:
    """
    Args:
        results (_type_): statsmodels RegressionResults object
        metrics (dict): dict from compute_metrics
        ticker (str): stock symbol, used for chart titles
    """
    
    figure = make_subplots(rows=3, cols=1)
    
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
    
    ### Panel 2
    
    
    ### Panel 3
    
    
    figure.show()
    