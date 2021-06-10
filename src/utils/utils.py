import streamlit as st


def create_container_time(key):
    with st.beta_container():
        startcol, endcol = st.beta_columns(2)

        with startcol:
            hour = startcol.selectbox(label='Hour', options=[i for i in range(0, 24)], key=key)

        with endcol:
            minutes = endcol.selectbox(label='Minutes', options=[i for i in range(0, 60)], key=key)
    return hour, minutes


def create_container_category(form_category, label):
    st.subheader(label)
    st.write(f'If {label.lower()} is not available, leave the checkbox unmarked and fill the field on the right.')
    with st.beta_container():
        startcol, endcol = st.beta_columns(2)
        with startcol:
            category_startcol = st.checkbox(label=f'Check this if the desired {label.lower()} is selected in the sidebar')
        with endcol:
            category_endcol = st.text_input(label=f'{label.title()}')
    if category_startcol:
        category = form_category
    else:
        category = category_endcol

    return category
