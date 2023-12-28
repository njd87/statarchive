import numpy as np
from scipy.stats import norm

"""
This object takes in several inputs and returns a bayesian linear regression estimator.

Parameters
    ----------
    x : data
        Independent variable observations
    y : data
        Dependent variable observations
    x_name : name of x data, default "x"
        Names x data
    y_name : name of y data, default "y"
        Names y data
    error : default = 1
        Assumes known error
    intercept : bool, default True
        Whether or not to include an intercept term

"""
class BayesianLinearRegression():
    # Initialize object
    def __init__(self, x, y, x_name : str, y_name : str, error : float):
        self.x = x
        self.y = y
        self.x_name = x_name
        self.y_name = y_name
        self.error = error
        self.posterior = None

    def fit(self):
        # Assume Normal: y | x = N(ax + b, sigma^2)
        pass