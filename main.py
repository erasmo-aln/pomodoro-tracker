import streamlit as st
import pandas as pd
import altair as alt
from utils import utils
from pages import track, create

FOLDER = 'data'
DATA = 'data.csv'
PATH_TO_DATA = '/'.join([FOLDER, DATA])


dataset = utils.get_dataset(PATH_TO_DATA)

st.set_page_config(layout="wide")

st.sidebar.title(body='Pomodoro Tracker')
select_option = st.sidebar.radio(label='Pages', options=['Home', 'Track', 'View', 'Create'], index=1)

# Homepage
if select_option == 'Home':
    st.title('Home')

# Fill Page
elif select_option == 'Track':

    with st.container():
        form_platform, form_subject, form_section = track.container(dataset)

    form = st.form('Data Form', clear_on_submit=True)
    with form:
        date, start_time, end_time, summary, submitted = track.form(form)

        if submitted:
            if track.assert_submitted([start_time, end_time]):
                track.save_dataset(date, start_time, end_time, form_platform, form_subject, form_section, summary, submitted)

    if submitted:
        with st.container():
            startcol, endcol = st.columns(2)
            startcol.write('The data was succesfully saved. To refresh the data, click the Refresh button.')
            endcol.button('Refresh')

# View Page
elif select_option == 'View':

    with st.container():
        platform, subject, _ = track.container(dataset)

    st.sidebar.title(body='Visualization Options')

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

    # Overall Plots
    if section == 'Overall':
        st.line_chart(data2show_grouped)

    # Section Plots
    elif section == 'Sections':
        st.altair_chart(chart_barh)

    # Show Summaries
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

# Create Data
elif select_option == 'Create':
    create.create_page()
