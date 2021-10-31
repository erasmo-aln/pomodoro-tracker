import streamlit as st

from pages import track


def create_page():
    col1, col2, col3 = st.columns(3)

    form_platform = col1.text_input(label='Platform')
    form_subject = col2.text_input(label='Subject')
    form_section = col3.text_input(label='Section')

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
