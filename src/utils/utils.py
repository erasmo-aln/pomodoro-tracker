from datetime import datetime as dt
import shutil


def print_help():
    terminal_width = shutil.get_terminal_size().columns
    title = 'Pomodoro Tracker Instructions'
    print()
    print(
        f'{title.center(terminal_width)}'
        f'{"-"*terminal_width}'
        f'{"Start and End time".center(terminal_width)}\n\n'
        f'{"The corresponding time of start and end of the Pomodoro. Example: 12:30 and 13:20.".center(terminal_width)}\n\n'
        f'{"Platform".center(terminal_width)}\n'
        f'{"The platform that you studied/worked, for example: Udacity, Udemy, Coursera etc.".center(terminal_width)}\n\n'
        f'{"Subject".center(terminal_width)}\n'
        f'{"The subject studied, for example: Machine Learning, Statistics, Python etc.".center(terminal_width)}\n\n'
        f'{"Section".center(terminal_width)}\n'
        f'''{"The current part that you're in. For example: Week 2, Chapter 5 and Project 2 etc.".center(terminal_width)}\n\n'''
        f'{"Total time".center(terminal_width)}\n'
        f'{"This is not a calculated field, so you need to enter the total time in minutes manually yet. This must be equal to the difference of end and start time.".center(terminal_width)}\n'
        f'{"-"*terminal_width}\n'
    )


def get_information():
    date_today = dt.today().strftime('%Y-%m-%d')
    begin = input("Start time: ")
    end = input("End time: ")
    platform = input("Platform: ")
    subject = input("Subject: ")
    section = input("Section: ")
    total = int(input("Total time: "))

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
