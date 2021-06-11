import pandas as pd
import os


def create_data_folder(folder):
    os.mkdir(folder)


def create_dataset(path_to_folder, filename):
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
    dataset.to_csv(f"{path_to_folder}/{filename}", sep=";", index=False)
