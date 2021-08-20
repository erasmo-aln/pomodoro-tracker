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

        # Start Time
        with st.container():
            startcol, endcol = st.columns(2)

            with startcol:
                start_time = st.time_input(label="Start time", value=dt.now())

            with endcol:
                end_time = st.time_input(label="End time", value=(dt.now() + timedelta(minutes=50)))

        # start_hour, start_min = utils.create_container_time(key='1')
        # start_hour = utils.check_length(start_hour)
        # start_min = utils.check_length(start_min)

        # End Time
        # st.subheader('End time')
        # end_hour, end_min = utils.create_container_time(key='2')
        # end_hour = utils.check_length(end_hour)
        # end_min = utils.check_length(end_min)

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

            total = (timedelta(hours=end_time.hour, minutes=end_time.minute) - timedelta(hours=start_time.hour, minutes=start_time.minute)).seconds // 60

            data_to_append = {
                "Date": [date],
                "Begin": [start_time.strftime("%H:%M")],
                "End": [end_time.strftime("%H:%M")],
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
        date_selected = st.selectbox(label='Select the date:', options=data2show.Date.unique())

        for index, row in data2show.loc[data2show.Date == date_selected].iterrows():
            time_header = f"From {row.Begin} to {row.End}:"
            st.subheader(time_header)
            st.write(row.Summary)
