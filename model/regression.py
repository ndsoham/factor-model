import statsmodels.api as sm
import pandas as pd

# regression equation
# excess_return = \alpha + \beta_1 * MktRF + \beta_2 * SMB + \beta_3 * HML + eps

def run_regression(stock_returns: pd.Series, factors: pd.DataFrame) -> any:
    """
    Args:
        stock_returns (pd.Series): pd.Series of daily stock returns named "stock_return"
        factors (pd.DataFrame): pd.DataFrame with columns Mkt-RF, SMB, HML, RF

    Returns:
        any: statsmodel RegressionResults object
    """
    
    aligned = pd.concat([stock_returns, factors], axis=1).dropna()
    aligned["excess"] = aligned["stock_return"] - aligned["RF"]
    
    X = aligned.loc[:, ["Mkt-RF", "SMB", "HML"]]
    X = sm.add_constant(X)
    
    y = aligned["excess"]
    
    results = sm.OLS(y, X).fit()
    return results, aligned
    
    
    