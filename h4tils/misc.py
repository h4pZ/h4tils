import os
import functools
import numpy as np
import pandas as pd
from datetime import datetime as dt


def get_project_path(module_path):
    """Gets the absolute path of the project folder.

    Parameters
    ----------
    module_path : str
        __file__ variable of the file that calls this function.

    Returns
    -------
    abs_project_path : str
        Absolute path of the project
    """
    src_path = os.path.dirname(module_path)
    abs_src_path = os.path.abspath(src_path)
    abs_project_path = os.path.dirname(abs_src_path)

    return abs_project_path


def timer(func):
    """Print the runtime of the decorated function.
    Taken from: https://realpython.com/primer-on-python-decorators/#timing-functions
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = dt.now()
        value = func(*args, **kwargs)
        end_time = dt.now()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time}")

        return value

    return wrapper_timer


def reduce_mem_usage(df, verbose=True):
    """Reduces the memory usage of a dataframe by assigning
    the minimum lower representation of a numeric column such that it doesn't
    lose information.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas data frame to optimize.
    verbose : bool, default True
        Whether to print the amount of memory saved.

    Returns
    -------
    df : pd.DataFrame
        The optimized dataframe.
    """

    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2

    for col in df.columns:
        col_type = df[col].dtypes

        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()

            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)

    end_mem = df.memory_usage().sum() / 1024**2

    if verbose:
        reduction = 100 * (start_mem - end_mem) / start_mem
        print(
            f'Mem. usage decreased to {end_mem:5.2f} Mb ({reduction:.1f}% reduction)')

    return df


def add_date_features(df, date_col, prefix="", drop=True, extra_features=None):
    """Extracts date features from a column in a dataframe and adds them to it.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas data frame to add the features.
    date_col : str
        Name of the column that holds the date data.
    prefix : str, optional
        Adds a prefix to the new created features.
    drop : bool, optional default True
        Whether to drop the original date column,
    extra_features : list, optional, default None
        List containing extra features to add to the dataframe.

    Returns
    -------
    df : pd.DataFrame
        Dataframe with the dates features added.
    """
    dates = df[date_col]

    features = ["year",
                "month",
                "week",
                "day",
                "dayofweek",
                "dayofyear",
                "is_month_end",
                "is_month_start",
                "is_quarter_end",
                "is_quarter_start",
                "is_year_end",
                "is_year_start"]

    if extra_features is not None:
        features += extra_features

    if not np.issubdtype(dates.dtype, np.datetime64):
        dates = pd.to_datetime(dates, infer_datetime_format=True)

    for feature in features:
        df[prefix + feature] = getattr(dates.dt, feature)

    if drop:
        df = df.drop(date_col, axis=1)

    return df


class AverageMeter:
    """
    Stores the current value, average and sum of a variable
    over `count` steps.

    Taken from:
    https://github.com/abhishekkrthakur/wtfml/blob/master/wtfml/utils/average_meter.py
    """

    def __init__(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
