from statsmodels.formula.api import ols
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
import seaborn as sns
import matplotlib.pyplot as plt

def product_transformations(x: str, y: str, data: pd.DataFrame, y_only: bool = True) -> tuple:
    """
    This function takes two variables and checks to see which transformation
    results in either: a) the highest R-squared value, or b) the lowest RSE.

    The transformations include:

        regular
        np.log
        np.sqrt
        np.square
        np.cube
        np.reciprocal
        np.reciprocal(np.sqrt)
        np.reciprocal(np.log)

    If y_only is True, then the function will only transform y. Otherwise, it checks all pairwise transformations

    Parameters
    ----------
    x : string
        The name of the first variable.
    y : string
        The name of the second variable.
    data : dataframe
        The dataframe containing the two variables.
    y_only : bool
        Whether or not to only transform y.
    
    Returns
    -------
    tuple
        A tuple containing the transformation with the highest R-squared value and the transformation with the lowest RSE.
    """
    # Create a list of all the transformations
    x_original = data[x]
    y_original = data[y]

    # list of transformation functions
    transformations_functions = {
        'original' : lambda x: x,
        'log' : np.log,
        'sqrt' : np.sqrt,
        'square' : np.square,
        'cube' : lambda x: np.power(x, 3),
        'reciprocal' : np.reciprocal,
        'reciprocal_sqrt' : lambda x: np.reciprocal(np.sqrt(x)),
        'reciprocal_log' : lambda x: np.reciprocal(np.log(x))
    }

    '''
    create a list of all transformation combinations as a dictionary
    keys look like: log_vs_original
    values look like: (r_squared, RSE), where r_squared and rse are the results of the statsmodels ols model fitted to the data described
    by the key (in the case given, it will be np.log(y) and x_original)
    '''

    transformation_combinations = {}
    if y_only:
        for name, func in transformations_functions.items():
            # if 1 or 0 are in the data, then the log and reciprocal functions will fail
            # so, if they are present, skip these functions and store the value as "(-1, float('inf'))"
            if (1 in y_original or 0 in y_original) and name in ['log', 'reciprocal', 'reciprocal_log']:
                transformation_combinations[f'{name}_vs_original'] = (-1, float('inf'))
                continue

            # create data frame
            df_curr = pd.DataFrame({'x' : x_original, 'y' : func(y_original)})
            # fit model
            model = ols('y ~ x', data=df_curr).fit()
            # store results
            transformation_combinations[f'{name}_vs_original'] = (model.rsquared, np.sqrt(model.mse_resid))
    else:
        # now, we do each pairwise combination of x and y
        for name_x, func_x in transformations_functions.items():
            for name_y, func_y in transformations_functions.items():
                # if 1 or 0 are in the data, then the log and reciprocal functions will fail
                # so, if they are present, skip these functions and store the value as "(-1, float('inf'))"
                if (1 in y_original or 0 in y_original) and name_y in ['log', 'reciprocal', 'reciprocal_log']:
                    transformation_combinations[f'{name_x}_vs_{name_y}'] = (-1, float('inf'))
                    continue

                # check the same for x
                if (1 in x_original or 0 in x_original) and name_x in ['log', 'reciprocal', 'reciprocal_log']:
                    transformation_combinations[f'{name_x}_vs_{name_y}'] = (-1, float('inf'))
                    continue

                # create data frame
                df_curr = pd.DataFrame({'x' : func_x(x_original), 'y' : func_y(y_original)})
                # fit model
                model = ols('y ~ x', data=df_curr).fit()
                # store results
                transformation_combinations[f'{name_x}_vs_{name_y}'] = (model.rsquared, np.sqrt(model.mse_resid))
        
    # find the transformation AND NAME with the highest r_squared
    max_r_squared = max(transformation_combinations.items(), key=lambda x: x[1][0])
    # find the transformation AND NAME with the lowest RSE
    min_rse = min(transformation_combinations.items(), key=lambda x: x[1][1])


    return max_r_squared, min_rse

        


if __name__ == '__main__':
    # import iris data
    iris = load_iris(as_frame=True)['frame']

    sns.scatterplot(data=iris, x='sepal length (cm)', y='sepal width (cm)')

    # get the transformation with the highest r_squared and the lowest RSE
    max_r_squared, min_rse = product_transformations('sepal length (cm)', 'sepal width (cm)', iris, y_only=False)

    print(f'The transformation with the highest r_squared is {max_r_squared[0]} with a value of {max_r_squared[1][0]}')
    print(f'The transformation with the lowest RSE is {min_rse[0]} with a value of {min_rse[1][1]}')
    
    plt.show()