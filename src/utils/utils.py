import streamlit as st
import pandas as pd
import os


def exists_path(path):
    return os.path.exists(path)


def create_folder(folder):
    os.makedirs(folder)


def create_dataset(path):
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
    dataset.to_csv(path, sep=";", index=False)


def get_dataset(path):

    filename = path.split('/')[-1]
    folder = path.replace(f'/{filename}', '')

    if not exists_path(path):
        if not exists_path(folder):
            create_folder(folder)
        create_dataset(path)

    dataset = pd.read_csv(path, sep=';')
    return dataset


def create_container_time(key):
    with st.beta_container():
        startcol, endcol = st.beta_columns(2)

        with startcol:
            hour_key = 'hour' + key
            hour = startcol.selectbox(label='Hour', options=[i for i in range(0, 24)], key=hour_key)

        with endcol:
            min_key = 'min' + key
            minutes = endcol.selectbox(label='Minutes', options=[i for i in range(0, 60)], key=min_key)
    return hour, minutes


def create_container_category(form_category, label):
    help_dict = {
        'Platform': 'The name of the platform (website, book, university) that you\'re studying. Examples: Udacity, Coursera, Udemy, MIT etc.',
        'Subject': 'The name of the subject/course that you\'re studying. Examples: Machine Learning, C++ Nanodegree, Deep Learning Specialization etc.',
        'Section': 'The chapter/section that you are currently in. Examples: Chapter 3, Lecture 5, Problem Set 2 etc.'
    }

    st.subheader(label)
    st.write(f'If {label.lower()} is not available, leave the checkbox unmarked and fill the field on the right.')
    with st.beta_container():
        startcol, endcol = st.beta_columns(2)
        with startcol:
            category_startcol = st.checkbox(label=f'Check this if the desired {label.lower()} is selected in the sidebar')
        with endcol:
            category_endcol = st.text_input(label=f'{label.title()}', help=help_dict[label])
    if category_startcol:
        category = form_category
    else:
        category = category_endcol
    return category


def is_filled(category):
    return bool(len(category))


def assert_fields(categories: list):
    for category in categories:
        if is_filled(category):
            continue
        else:
            return False
    return True


def check_length(time):
    time = str(time)
    if len(time) == 1:
        time = str(0) + time
        return time
    else:
        return time
