import os

import pandas as pd

import utils


while True:
    utils.print_help()
    data_to_append = utils.get_information()

    confirmed = False
    while confirmed is False:
        utils.print_confirmation_data(data_dict=data_to_append)
        ask_to_confirm = input('Answer [y/n]: ').lower()

        if ask_to_confirm == 'y':
            confirmed = True
        else:
            index_item = int(input('Which item do you want to change? [1 to 7]\nAnswer: '))
            data_to_append = utils.change_selected_item(data_dict=data_to_append, index=index_item)

    data_to_append_dataframe = pd.DataFrame.from_dict(data=data_to_append)

    data_to_append_dataframe.to_csv(path_or_buf="../data/dataset.csv", sep=";", index=False, mode="a", header=False)

    ask_to_repeat = input("Do you want to add another record? [y/n]: ").lower()
    if ask_to_repeat == "n":
        break
    else:
        os.system('cls')
