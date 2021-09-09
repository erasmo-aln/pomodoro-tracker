from datetime import datetime as dt
from datetime import timedelta
import streamlit as st
import pandas as pd
import altair as alt
from src.utils import utils


FOLDER = 'data'
DATA = 'data.csv'
PATH_TO_DATA = '/'.join([FOLDER, DATA])


dataset = utils.get_dataset(PATH_TO_DATA)

st.title(body='Pomodoro Tracker')
select_option = st.radio(label='Fill or View?', options=['Fill', 'View'])

submitted = False

if select_option == 'Fill':
    st.sidebar.title(body='Information Available')

    form_platform = st.sidebar.radio(label='Platforms', options=list(dataset.Platform.unique()))
    form_subject = st.sidebar.radio(label='Subjects', options=list(dataset.Subject.loc[dataset.Platform == form_platform].unique()))
    form_section = st.sidebar.radio(label='Sections', options=list(dataset.Section.loc[(dataset.Platform == form_platform) & (dataset.Subject == form_subject)].unique()))

    with st.form('Data Form'):
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

        # Platform
        platform = utils.create_container_category(form_category=form_platform, label='Platform')

        # Subject
        subject = utils.create_container_category(form_category=form_subject, label='Subject')

        # Section
        section = utils.create_container_category(form_category=form_section, label='Section')

        # Summary
        summary = st.text_area(label='Summary', help='A brief summary of what you studied in this Pomodoro. *This is an optional field.*', height=200)

        submitted = st.form_submit_button("Submit")

    # Append to dataset here
    categories = [platform, subject, section]
    if submitted:
        if not utils.assert_fields(categories):
            st.warning('You left 1 or more fields blank. Please fill them in.')
        else:

            total = (timedelta(hours=dt.strptime(end_time, '%H:%M').hour, minutes=dt.strptime(end_time, '%H:%M').minute) - timedelta(hours=dt.strptime(start_time, '%H:%M').hour, minutes=dt.strptime(start_time, '%H:%M').minute)).seconds // 60

            data_to_append = {
                "Date": [date],
                "Begin": [start_time],
                "End": [end_time],
                "Platform": [platform],
                "Subject": [subject],
                "Section": [section],
                "Summary": [summary],
                "Total": [total]
            }

            data_to_append_dataframe = pd.DataFrame.from_dict(data=data_to_append)
            data_to_append_dataframe.to_csv(path_or_buf=PATH_TO_DATA, sep=";", index=False, mode="a", header=False)

            with st.container():
                startcol, endcol = st.columns(2)
                startcol.write('The data was succesfully saved. To refresh the data, click the Refresh button.')
                endcol.button('Refresh')

else:
    st.sidebar.title(body='Visualization Options')

    platform = st.sidebar.radio(label='Platform', options=list(dataset.Platform.unique()))
    subject = st.sidebar.radio(label='Subject', options=list(dataset.Subject.loc[dataset.Platform == platform].unique()))
    section = st.sidebar.radio(label='Choose the chart', options=['Overall', 'Sections', 'Summaries'])

    data2show = dataset.loc[(dataset.Platform == platform) & (dataset.Subject == subject)]

    data2show_grouped = data2show.groupby('Date')['Total'].sum()

    data2show_grouped2 = data2show.groupby('Section')['Total'].sum()

    chart_barh = alt.Chart(
        data2show_grouped2.reset_index()
        ).mark_bar().encode(
            x=alt.X('sum(Total):Q', axis=alt.Axis(title='Total (in minutes)')),
            y=alt.Y('Section', axis=alt.Axis(title=''))
            ).properties(width=700, height=300).configure_axis(grid=False)

    if section == 'Overall':
        st.line_chart(data2show_grouped)

    elif section == 'Sections':
        st.altair_chart(chart_barh)

    elif section == 'Summaries':
        # date_selected = st.selectbox(label='Select the date:', options=data2show.Date.unique())
        dates_available = data2show.Date.unique()
        total_days = len(dates_available)
        total_pomodoros = len(data2show)
        total_minutes = data2show.Total.sum()

        st.markdown(f"## Over the course of {total_days} day(s), you applied {total_pomodoros} Pomodoro(s), resulting in a total of {total_minutes} minutes studied.")
        st.markdown("---")

        for number, date in enumerate(dates_available):
            with st.container():
                st.header(f'{pd.to_datetime(date).strftime("%d/%m/%Y")} - {pd.to_datetime(date).strftime("%A")}')
                POMODORO_INDEX = 1
                for index, row in data2show.loc[data2show.Date == date].iterrows():
                    time_header = f"Pomodoro {POMODORO_INDEX} - {row.Begin} to {row.End}"
                    st.subheader(time_header)
                    if pd.isnull(row.Summary) or row.Summary == '':
                        st.write("No Summary.")
                    else:
                        st.markdown(f"**Summary**: \n{row.Summary}")
                    POMODORO_INDEX += 1
                st.markdown("---")
