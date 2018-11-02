import pandas as pd

def check_types_pretty(df):
    # Printing types of all columns in df in a pretty way
    for col in df.columns:
        print("* {0:16}  \t\t | {1} ".format(col, type(df[col][0])))

def calculate_trip_duration(df):
    """
    Function returns a dataframe with additional column 'trip_duration'.
    'trip_duration' is a time in minutes between tpep_pickup_datetime and tpep_dropoff_datetime
    """
    # Converting colums from 'string' type to 'datetime' type
    drop_off = pd.to_datetime(df.tpep_dropoff_datetime)
    pick_up = pd.to_datetime(df.tpep_pickup_datetime)

    # Adding a new column 'duration' converted to minutes [m]
    df['duration'] = (drop_off - pick_up).astype('timedelta64[m]')
    return df
