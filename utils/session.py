import streamlit as st


def initialise_session():

    defaults = {

        "active_view": "home",

        "recommendations": None,

        "history": [],

        "selected_skin_type": None,

        "selected_issue": None

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value