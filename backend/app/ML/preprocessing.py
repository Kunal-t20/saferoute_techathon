import pandas as pd

def preprocess_data(path):

    df = pd.read_csv(path)

    # ----- DATE FEATURES -----
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df['hour'] = pd.to_datetime(df['time'], errors='coerce').dt.hour

    df = df.dropna(subset=['date', 'hour'])

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    df.drop(['date','time','accident_index'], axis=1, inplace=True)

    # ----- TARGET -----
    y = df['accident_severity']
    X = df.drop('accident_severity', axis=1)

    return X, y
