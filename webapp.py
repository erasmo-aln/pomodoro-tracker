import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
from src.utils import utils
import os

PATH_TO_FOLDER = 'data'
PATH_TO_DATA = 'data/dataset.csv'

try:
    dataset = utils.read_dataset(PATH_TO_DATA)

except FileNotFoundError:
    if not os.path.exists(PATH_TO_FOLDER):
        utils.create_data_folder(PATH_TO_FOLDER)
    utils.create_dataset(PATH_TO_DATA)
    dataset = utils.read_dataset(PATH_TO_DATA)

st.title(body='Pomodoro Tracker')
select_option = st.radio(label='Fill or View?', options=['Fill', 'View'])
submitted = False

if select_option == 'Fill':
    form_platform = st.sidebar.radio(label='Platforms Available', options=list(dataset.Platform.unique()))
    form_subject = st.sidebar.radio(label='Subjects Available', options=list(dataset.Subject.loc[dataset.Platform == form_platform].unique()))
    form_section = st.sidebar.radio(label='Sections Available', options=list(dataset.Section.loc[(dataset.Platform == form_platform) & (dataset.Subject == form_subject)].unique()))
    with st.form('Data Form'):
        date_today = dt.today().strftime('%Y-%m-%d')
        st.write("Fill out the information about your Pomodoro")

        # Start Time
        st.subheader('Start time')
        start_hour, start_min = utils.create_container_time(key=1)

        # End Time
        st.subheader('End time')
        end_hour, end_min = utils.create_container_time(key=2)

        # Platform
        platform = utils.create_container_category(form_category=form_platform, label='Platform')

        # Subject
        subject = utils.create_container_category(form_category=form_subject, label='Subject')

        # Section
        section = utils.create_container_category(form_category=form_section, label='Section')

        submitted = st.form_submit_button("Submit")

    # Append to dataset here
    if submitted:
        start_time = f'{start_hour}:{start_min}'
        end_time = f'{end_hour}:{end_min}'
        total = (end_hour * 60 + end_min) - (start_hour * 60 + start_min)
        data_to_append = {
            "Date": [date_today],
            "Begin": [start_time],
            "End": [end_time],
            "Platform": [platform],
            "Subject": [subject],
            "Section": [section],
            "Total": [total]
        }
        data_to_append_dataframe = pd.DataFrame.from_dict(data=data_to_append)
        data_to_append_dataframe.to_csv(path_or_buf="data/data.csv", sep=";", index=False, mode="a", header=False)

        with st.beta_container():
            startcol, endcol = st.beta_columns(2)
            startcol.write('The data was succesfully saved. To refresh the data, click the button at the right.')
            endcol.button('Rerun')

else:
    st.sidebar.title(body='Visualization Options')

    platform = st.sidebar.radio(label='Platform', options=list(dataset.Platform.unique()))
    subject = st.sidebar.radio(label='Subject', options=list(dataset.Subject.loc[dataset.Platform == platform].unique()))
    section = st.sidebar.radio(label='Choose the chart', options=['Overall', 'Sections'])

    data2show = dataset.loc[(dataset.Platform == platform) & (dataset.Subject == subject)]
    data2show_grouped = data2show.groupby('Date')['Total'].sum()
    data2show_grouped2 = data2show.groupby('Section')['Total'].sum()

    chart_barh = alt.Chart(data2show_grouped2.reset_index()).mark_bar().encode(
        x=alt.X('sum(Total):Q', axis=alt.Axis(title='Total (in minutes)')),
        y=alt.Y('Section', axis=alt.Axis(title=''))
    ).properties(
        width=700,
        height=300
    ).configure_axis(
        grid=False
    )

    if section == 'Sections':
        st.altair_chart(chart_barh)
    else:
        st.line_chart(data2show_grouped)
