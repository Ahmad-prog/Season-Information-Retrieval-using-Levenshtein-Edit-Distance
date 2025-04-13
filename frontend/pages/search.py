import streamlit as st
import sys
import os
from PIL import Image

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database import search_dramas
from backend.levenshtein import levenshtein_distance


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
    st.markdown("<h1 class='main-header'>Search Pakistani Dramas</h1>", unsafe_allow_html=True)

    # Explanation of fuzzy search
    with st.expander("About Fuzzy Search"):
        st.markdown("""
        This search engine uses **Levenshtein Edit Distance** to find dramas even when the search term is misspelled.

        ### What is Levenshtein Edit Distance?

        The Levenshtein distance is a measure of the difference between two strings. It represents the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one string into another.

        ### Why is this useful for Pakistani dramas?

        Many Pakistani dramas have Urdu titles written in English, which can be spelled in different ways. For example, "Andhera Ujala" might be typed as "Andera Ujhala" or "Undera Ujala". Our fuzzy search will find the correct drama regardless of these variations.

        ### How to use:

        1. Enter a drama title or director name in the search box
        2. Adjust the fuzzy matching threshold if needed (lower values = more matches)
        3. Click Search
        """)

    st.markdown("<div class='search-box'>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])

    with col1:
        search_term = st.text_input("Enter drama title or director name", label_visibility="collapsed")

    with col2:
        fuzzy_threshold = st.slider("Fuzzy Match Threshold", 0.0, 1.0, 0.3, 0.1,
                                    help="Lower values will match more variations (0.0-1.0)")

    search_button = st.button("Search")
    st.markdown("</div>", unsafe_allow_html=True)

    if search_term and search_button:
        dramas = search_dramas(search_term, fuzzy_threshold)

        if dramas:
            st.markdown(f"<h3 class='sub-header'>Found {len(dramas)} results for '{search_term}'</h3>",
                        unsafe_allow_html=True)

            # If using fuzzy matching, show the Levenshtein distance for each match
            if fuzzy_threshold < 1.0:
                st.markdown("### Match Details")
                match_details = []

                for drama in dramas:
                    title_distance = levenshtein_distance(search_term.lower(), drama['title'].lower())
                    director_distance = levenshtein_distance(search_term.lower(), drama['director'].lower())
                    min_distance = min(title_distance, director_distance)

                    # Also check words in title
                    for word in drama['title'].lower().split():
                        word_distance = levenshtein_distance(search_term.lower(), word)
                        min_distance = min(min_distance, word_distance)

                    match_details.append({
                        "Drama": drama['title'],
                        "Levenshtein Distance": min_distance
                    })

                # Display match details in a table
                st.table(match_details)

            for drama in dramas:
                display_drama_card(drama)
        else:
            st.info(
                f"No dramas found matching '{search_term}'. Try a different search term or adjust the fuzzy matching threshold.")
    else:
        st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <p style='font-size: 18px; color: #6B7280;'>
                Enter a drama title or director name to search the database.
            </p>
            <p style='font-size: 16px; color: #6B7280;'>
                Our fuzzy search will find matches even if you misspell the title!
            </p>
            <p style='font-size: 14px; color: #9CA3AF;'>
                Examples: Try searching for "Andera Ujala" instead of "Andhera Ujala" or "Zindgi Gulzar" instead of "Zindagi Gulzar Hai"
            </p>
        </div>
        """, unsafe_allow_html=True)
