
def compute_metrics(results) -> dict:
    """

    Args:
        results (_type_): statsmodel RegressionResults object from run_regression

    Returns:
        dict with keys:
            - alpha     : intercept (annualized)
            - beta_mkt  : sensitivity to market factor
            - beta_smb  : sensitivity to size factor
            - beta_hml  : sensitivity to value factor
            - r_squared : proportion of return variance explained by factors
            - t_stats   : dict of t-statistics for each coefficient
            - p_values  : dict of p_values for each coefficient
    """
    
    metrics = dict()
    
    metrics["alpha"] = (1 + results.params["const"])**252 - 1
    metrics["beta_mkt"] = results.params["Mkt-RF"]
    metrics["beta_smb"] = results.params["SMB"]
    metrics["beta_hml"] = results.params["HML"]
    metrics["r_squared"] = results.rsquared
    metrics["t_stats"] = results.tvalues.to_dict()
    metrics["p_values"] = results.pvalues.to_dict()
    
    return metrics