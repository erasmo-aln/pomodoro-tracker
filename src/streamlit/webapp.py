import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
import numpy as np


dataset = pd.read_csv('data/dataset.csv', sep=';')

st.title(body='Pomodoro Tracker')
select_option = st.radio(label='Fill or View?', options=['Fill', 'View'])

form_platform = st.sidebar.radio(label='Platforms Available', options=list(dataset.Platform.unique()))
form_subject = st.sidebar.radio(label='Subjects Available', options=list(dataset.Subject.loc[dataset.Platform == form_platform].unique()))
form_section = st.sidebar.radio(label='Sections Available', options=list(dataset.Section.loc[(dataset.Platform == form_platform) & (dataset.Subject == form_subject)].unique()))
submitted = False

if select_option == 'Fill':
    with st.form('Fill form'):
        date_today = dt.today().strftime('%Y-%m-%d')
        st.write("Fill out the information")

        # Start Time
        st.subheader('Start time')
        with st.beta_container():
            startcol, endcol = st.beta_columns(2)

            with startcol:
                start_hour = startcol.selectbox(label='Hour', options=[i for i in range(0, 24)], key=1)

            with endcol:
                start_min = endcol.selectbox(label='Minutes', options=[i for i in range(0, 60)], key=1)

        # End Time
        st.subheader('End time')
        with st.beta_container():
            startcol, endcol = st.beta_columns(2)

            with startcol:
                end_hour = startcol.selectbox(label='Hour', options=[i for i in range(0, 24)], key=2)

            with endcol:
                end_min = endcol.selectbox(label='Minutes', options=[i for i in range(0, 60)], key=2)

        # Platform
        st.subheader('Platform')
        st.write('If platform is not available, leave the checkbox unmarked and fill the field on the right.')
        with st.beta_container():
            startcol, endcol = st.beta_columns(2)
            with startcol:
                platform_startcol = st.checkbox(label='Check this if the desired platform is selected in the sidebar')
            with endcol:
                platform_endcol = st.text_input(label='Platform')
        if platform_startcol:
            platform = form_platform
        else:
            platform = platform_endcol

        # Subject
        st.subheader('Subject')
        st.write('If subject is not available, leave the checkbox unmarked and fill the field on the right.')
        with st.beta_container():
            startcol, endcol = st.beta_columns(2)
            with startcol:
                subject_startcol = st.checkbox(label='Check this if the desired subject is selected in the sidebar')
            with endcol:
                subject_endcol = st.text_input(label='Subject')
        if subject_startcol:
            subject = form_subject
        else:
            subject = subject_endcol

        # Section
        st.subheader('Section')
        st.write('If section is not available, leave the checkbox unmarked and fill the field on the right.')
        with st.beta_container():
            startcol, endcol = st.beta_columns(2)
            with startcol:
                section_startcol = st.checkbox(label='Check this if the desired section is selected in the sidebar')
            with endcol:
                section_endcol = st.text_input(label='Section')
        if section_startcol:
            section = form_section
        else:
            section = section_endcol

        total = (end_hour*60 + end_min) - (start_hour*60 + start_min)

        submitted = st.form_submit_button("Submit")

    # Append to dataset here
    if submitted:
        start_time = f'{start_hour}:{start_min}'
        end_time = f'{end_hour}:{end_min}'
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
        data_to_append_dataframe.to_csv(path_or_buf="data/dataset.csv", sep=";", index=False, mode="a", header=False)
        st.dataframe(pd.DataFrame.from_dict(data_to_append))
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


# with st.form('my form'):
#     st.write("Inside the form")
#     st.text_input('Data: ')

#     submitted = st.form_submit_button("Submit")