from datetime import datetime as dt


def get_information():
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

    return data_to_append


def print_confirmation_data(data_dict):
    print('\nDo you confirm the information below?')
    print(
        f'[1] Date: {data_dict["Date"][0]}\n'
        f'[2] Begin: {data_dict["Begin"][0]}\n'
        f'[3] End: {data_dict["End"][0]}\n'
        f'[4] Platform: {data_dict["Platform"][0]}\n'
        f'[5] Subject: {data_dict["Subject"][0]}\n'
        f'[6] Section: {data_dict["Section"][0]}\n'
        f'[7] Total: {data_dict["Total"][0]}'
    )


def change_selected_item(data_dict, index):
    key = list(data_dict.keys())[index - 1]

    print(f'\nYou selected {key}')
    print(f'Old value: {data_dict[key][0]}')

    new_data = input('New value: ')
    data_dict.update({key: [new_data]})

    return data_dict
