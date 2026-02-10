import pandas as pd 


def preprocess(File_path):

    df=pd.read_csv(File_path)
    
    df = pd.get_dummies(df)

    return df




