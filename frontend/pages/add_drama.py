import streamlit as st
import sys
import os

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database import add_drama


def app():
    st.markdown("<h1 class='main-header'>Add New Drama</h1>", unsafe_allow_html=True)

    with st.form("add_drama_form"):
        st.markdown("<h3 class='form-header'>Drama Details</h3>", unsafe_allow_html=True)

        title = st.text_input("Title", max_chars=255)
        director = st.text_input("Director", max_chars=255)
        year = st.number_input("Year", min_value=1950, max_value=2023, value=2020)
        channel = st.text_input("Channel", max_chars=100)
        episodes = st.number_input("Number of Episodes", min_value=1, value=20)
        rating = st.slider("Rating", min_value=1.0, max_value=10.0, value=8.0, step=0.1)
        description = st.text_area("Description", height=150)

        # For simplicity, we'll just ask for an image path
        image_path = st.text_input("Image Path (local file path)", value="images/placeholder.jpg")

        submitted = st.form_submit_button("Add Drama")

        if submitted:
            if not title or not director:
                st.error("Title and Director are required fields.")
            else:
                drama_id = add_drama(title, director, year, channel, episodes, rating, description, image_path)

                if drama_id:
                    st.success(f"Drama '{title}' added successfully with ID: {drama_id}")
                else:
                    st.error("Failed to add drama. Please check your inputs and try again.")
