import pandas as pd
from datetime import datetime as dt


while True:

    date_today = dt.today().strftime('%Y-%m-%d')
    begin = input("Start time (for example, 13:47): ")
    end = input("End time (for example, 14:37): ")
    platform = input("Platform (DSA, MIT OCW...): ")
    subject = input("Subject (Machine Learning, Probability...): ")
    section = input("Section (Chapter 3, Lecture 5...): ")
    total = int(input("Total time (in minutes): "))

    data_to_append = {
        "Date": [date_today],
        "Begin": [begin],
        "End": [end],
        "Platform": [platform],
        "Subject": [subject],
        "Section": [section],
        "Total": [total]
    }

    data_to_append_dataframe = pd.DataFrame.from_dict(data=data_to_append)

    data_to_append_dataframe.to_csv(path_or_buf="../data/dataset.csv", sep=";", index=False, mode="a", header=False)

    answer = input("Do you want to add another record? [y/n]: ")
    if answer == "n" or answer == "N":
        break
    else:
        print("-" * 40)
