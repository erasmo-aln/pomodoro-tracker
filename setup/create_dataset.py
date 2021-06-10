import pandas as pd
import os


os.mkdir('data')
columns = {
    "Date": pd.Series([], dtype="object"),
    "Begin": pd.Series([], dtype="object"),
    "End": pd.Series([], dtype="object"),
    "Platform": pd.Series([], dtype="object"),
    "Subject": pd.Series([], dtype="object"),
    "Section": pd.Series([], dtype="object"),
    "Total": pd.Series([], dtype="int32")
}

dataset = pd.DataFrame.from_dict(columns)
dataset.to_csv("data/data.csv", sep=";", index=False)
