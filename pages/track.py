import streamlit as st
from datetime import timedelta
from utils import utils
import pandas as pd
from datetime import datetime as dt


def title():
    st.sidebar.title(body='Fill Options')
    st.sidebar.radio(label='Options', options=['New', 'Edit', 'Delete'])


def container(dataset):
    col1, col2, col3 = st.columns(3)

    form_platform = col1.selectbox(label='Platforms', options=list(dataset.Platform.unique()))
    form_subject = col2.selectbox(label='Subjects', options=list(dataset.Subject.loc[dataset.Platform == form_platform].unique()))
    form_section = col3.selectbox(label='Sections', options=list(dataset.Section.loc[(dataset.Platform == form_platform) & (dataset.Subject == form_subject)].unique()))

    return form_platform, form_subject, form_section


def form(form):
    submitted = False
    st.write("Fill out the information about your Pomodoro")

    st.subheader("Date and Time:")
    date = st.date_input(label="Date:").strftime('%Y-%m-%d')

    # Start and End Time
    with st.container():
        startcol, endcol = st.columns(2)

        with startcol:
            start_time = st.text_input(label="Start time")

        with endcol:
            end_time = st.text_input(label="End time")

    # Summary
    summary = st.text_area(label='Summary', help='A brief summary of what you studied in this Pomodoro. *This is an optional field.*', height=200)

    submitted = form.form_submit_button("Submit")

    return date, start_time, end_time, summary, submitted


def assert_submitted(categories):
    if not utils.assert_fields(categories):
        st.warning('You left 1 or more fields blank. Please fill them in.')

        return False

    return True


def save_dataset(date, start_time, end_time, form_platform, form_subject, form_section, summary, submitted):
    FOLDER = 'data'
    DATA = 'data.csv'
    PATH_TO_DATA = '/'.join([FOLDER, DATA])

    total = (timedelta(hours=dt.strptime(end_time, '%H:%M').hour, minutes=dt.strptime(end_time, '%H:%M').minute) - timedelta(hours=dt.strptime(start_time, '%H:%M').hour, minutes=dt.strptime(start_time, '%H:%M').minute)).seconds // 60

    data_to_append = {
        "Date": [date],
        "Begin": [start_time],
        "End": [end_time],
        "Platform": [form_platform],
        "Subject": [form_subject],
        "Section": [form_section],
        "Summary": [summary],
        "Total": [total]
    }

    data_to_append_dataframe = pd.DataFrame.from_dict(data=data_to_append)
    data_to_append_dataframe.to_csv(path_or_buf=PATH_TO_DATA, sep=";", index=False, mode="a", header=False)

# def fill(dataset):

#     with st.container():
#         col1, col2, col3 = st.columns(3)

#         form_platform = col1.selectbox(label='Platforms', options=list(dataset.Platform.unique()))
#         form_subject = col2.selectbox(label='Subjects', options=list(dataset.Subject.loc[dataset.Platform == form_platform].unique()))
#         form_section = col3.selectbox(label='Sections', options=list(dataset.Section.loc[(dataset.Platform == form_platform) & (dataset.Subject == form_subject)].unique()))

#     form = st.form('Data Form', clear_on_submit=True)
#     with form:
#         st.write("Fill out the information about your Pomodoro")

#         st.subheader("Date and Time:")
#         date = st.date_input(label="Date:").strftime('%Y-%m-%d')

#         # Start and End Time
#         with st.container():
#             startcol, endcol = st.columns(2)

#             with startcol:
#                 start_time = st.text_input(label="Start time")

#             with endcol:
#                 end_time = st.text_input(label="End time")

#         # Summary
#         summary = st.text_area(label='Summary', help='A brief summary of what you studied in this Pomodoro. *This is an optional field.*', height=200)

#         submitted = form.form_submit_button("Submit")

    # Append to dataset here
    # categories = [start_time, end_time]
    # if submitted:
    #     if not utils.assert_fields(categories):
    #         st.warning('You left 1 or more fields blank. Please fill them in.')
    #     else:

    #         total = (timedelta(hours=dt.strptime(end_time, '%H:%M').hour, minutes=dt.strptime(end_time, '%H:%M').minute) - timedelta(hours=dt.strptime(start_time, '%H:%M').hour, minutes=dt.strptime(start_time, '%H:%M').minute)).seconds // 60

    #         data_to_append = {
    #             "Date": [date],
    #             "Begin": [start_time],
    #             "End": [end_time],
    #             "Platform": [form_platform],
    #             "Subject": [form_subject],
    #             "Section": [form_section],
    #             "Summary": [summary],
    #             "Total": [total]
    #         }

    #         data_to_append_dataframe = pd.DataFrame.from_dict(data=data_to_append)
    #         data_to_append_dataframe.to_csv(path_or_buf=PATH_TO_DATA, sep=";", index=False, mode="a", header=False)

    #         with st.container():
    #             startcol, endcol = st.columns(2)
    #             startcol.write('The data was succesfully saved. To refresh the data, click the Refresh button.')
    #             endcol.button('Refresh')