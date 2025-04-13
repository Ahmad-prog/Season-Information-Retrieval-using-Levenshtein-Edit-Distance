import streamlit as st
import sys
import os
from PIL import Image

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database import get_all_dramas


def display_drama_card(drama):
    col1, col2 = st.columns([1, 3])

    with col1:
        # Check if image exists, otherwise show placeholder
        image_path = drama['image_path']
        if os.path.exists(image_path):
            try:
                image = Image.open(image_path)
                st.image(image, width=200)
            except Exception as e:
                st.image("https://via.placeholder.com/200x300?text=No+Image", width=200)
        else:
            st.image("https://via.placeholder.com/200x300?text=No+Image", width=200)

    with col2:
        st.markdown(f"<h3 class='drama-title'>{drama['title']} ({drama['year']})</h3>", unsafe_allow_html=True)
        st.markdown(f"<p class='drama-info'><strong>Director:</strong> {drama['director']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='drama-info'><strong>Channel:</strong> {drama['channel']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='drama-info'><strong>Episodes:</strong> {drama['episodes']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='drama-rating'><strong>Rating:</strong> {drama['rating']}/10</p>",
                    unsafe_allow_html=True)
        st.markdown(f"<p class='drama-description'>{drama['description']}</p>", unsafe_allow_html=True)

    st.markdown("---")


def app():
    st.markdown("<h1 class='main-header'>All Pakistani Dramas</h1>", unsafe_allow_html=True)

    dramas = get_all_dramas()

    if dramas:
        # Sort options
        sort_option = st.selectbox(
            "Sort by:",
            ["Title (A-Z)", "Title (Z-A)", "Year (Newest)", "Year (Oldest)", "Rating (Highest)", "Rating (Lowest)"]
        )

        if sort_option == "Title (A-Z)":
            dramas = sorted(dramas, key=lambda x: x['title'])
        elif sort_option == "Title (Z-A)":
            dramas = sorted(dramas, key=lambda x: x['title'], reverse=True)
        elif sort_option == "Year (Newest)":
            dramas = sorted(dramas, key=lambda x: x['year'], reverse=True)
        elif sort_option == "Year (Oldest)":
            dramas = sorted(dramas, key=lambda x: x['year'])
        elif sort_option == "Rating (Highest)":
            dramas = sorted(dramas, key=lambda x: x['rating'], reverse=True)
        elif sort_option == "Rating (Lowest)":
            dramas = sorted(dramas, key=lambda x: x['rating'])

        for drama in dramas:
            display_drama_card(drama)
    else:
        st.info("No dramas found in the database. Please add some dramas first.")
