import streamlit as st
import sys
import os

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.database import get_all_dramas, search_dramas, get_all_tags, get_dramas_by_tag
from backend.levenshtein import levenshtein_distance
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="Pakistani Drama Database",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with sidebar collapsed
)


# Load CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "style.css")
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Add custom CSS for tags
    st.markdown("""
    <style>
    .drama-tags {
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .tag {
        display: inline-block;
        background-color: #f0f0f0;
        color: #333;
        padding: 4px 10px;
        border-radius: 15px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .tag:hover {
        background-color: #e0e0e0;
    }
    .tag-active {
        background-color: #4CAF50;
        color: white;
    }
    .tag-cloud {
        margin: 20px 0;
        padding: 15px;
        background-color: #f9f9f9;
        border-radius: 10px;
        text-align: center;
    }
    .tag-cloud-title {
        margin-bottom: 15px;
        font-size: 1.2rem;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)


load_css()

# Custom header with logo and title
st.markdown("""<div class="custom-header">
    <div class="logo-container">
        <span class="logo-text">🎭</span>
    </div>
    <div class="title-container">
        <h1 class="site-title">Pakistani Drama Database</h1>
        <p class="site-subtitle">Discover the rich world of Pakistani television</p>
    </div>
</div>""", unsafe_allow_html=True)

# Top navigation with radio buttons
st.markdown('<div class="top-nav">', unsafe_allow_html=True)
page = st.radio("", ["Home", "View All Dramas", "Browse by Tags", "Add New Drama", "Search Dramas"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)


# Function to display drama cards with tags
def display_drama_card(drama):
    st.markdown('<div class="drama-card">', unsafe_allow_html=True)
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

        # Display tags if available
        if 'tags' in drama and drama['tags']:
            tags_html = '<div class="drama-tags">'
            for tag in drama['tags']:
                # Make each tag clickable with a query parameter
                tags_html += f'<a href="?tag={tag}" target="_self"><span class="tag">{tag}</span></a>'
            tags_html += '</div>'
            st.markdown(tags_html, unsafe_allow_html=True)

        st.markdown(f"<p class='drama-description'>{drama['description']}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# Check if a tag was clicked and redirect to Browse by Tags page
query_params = st.experimental_get_query_params()
if "tag" in query_params:
    selected_tag = query_params["tag"][0]
    page = "Browse by Tags"
    st.experimental_set_query_params()  # Clear query params after processing

# Home Page
if page == "Home":
    # Hero section
    st.markdown("""
    <div class="hero-section" style="background-color: #1E3A8A; color: white; padding: 40px; border-radius: 10px; text-align: center; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <h2 style="color: white; font-size: 2.2rem; margin-bottom: 15px;">Welcome to the Pakistani Drama Database!</h2>
        <p style="color: white; font-size: 1.2rem; max-width: 800px; margin: 0 auto;">Explore the rich world of Pakistani television dramas with our comprehensive database</p>
    </div>
    """, unsafe_allow_html=True)

    # Features section
    st.markdown("""
    <div class="features-section">
        <h2>Features</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3>Smart Search</h3>
                <p>Find dramas even with misspelled titles using our fuzzy search technology</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📺</div>
                <h3>Comprehensive Database</h3>
                <p>Browse through a rich collection of Pakistani dramas from various eras</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🏷️</div>
                <h3>Browse by Tags</h3>
                <p>Discover dramas by genre, era, channel, and more using our tagging system</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">➕</div>
                <h3>Contribute</h3>
                <p>Add new dramas to our growing database and help preserve Pakistani TV history</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tag cloud section
    st.markdown("<h2 class='section-header'>Popular Tags</h2>", unsafe_allow_html=True)
    all_tags = get_all_tags()
    if all_tags:
        st.markdown('<div class="tag-cloud">', unsafe_allow_html=True)
        tags_html = ""
        for tag in all_tags[:15]:  # Show top 15 tags
            tags_html += f'<a href="?tag={tag}" target="_self"><span class="tag">{tag}</span></a>'
        st.markdown(tags_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Featured dramas section
    st.markdown("<h2 class='section-header'>Featured Dramas</h2>", unsafe_allow_html=True)
    # Get top 3 highest rated dramas
    dramas = get_all_dramas()
    if dramas:
        top_dramas = sorted(dramas, key=lambda x: x['rating'], reverse=True)[:3]
        for drama in top_dramas:
            display_drama_card(drama)
    else:
        st.info("No dramas found in the database. Please add some dramas first.")

    # Add a section about fuzzy search
    st.markdown("<h2 class='section-header'>Fuzzy Search Technology</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <h3>What is Levenshtein Edit Distance?</h3>
        <p>
            The Levenshtein distance is a string metric for measuring the difference between two sequences.
            It calculates the minimum number of single-character edits (insertions, deletions, or substitutions)
            required to change one word into another.
        </p>
        <h3>Why is this useful for Pakistani dramas?</h3>
        <p>
            Many Pakistani dramas have Urdu titles written in English, which can be spelled in different ways.
            For example, "Andhera Ujala" might be typed as "Andera Ujhala" or "Undera Ujala".
            Our fuzzy search will find the correct drama regardless of these variations.
        </p>
        <h3>Example:</h3>
        <p>
            If you search for "Zindgi Gulzar", our system will still find "Zindagi Gulzar Hai" because
            the Levenshtein distance between these terms is small enough to be considered a match.
        </p>
    </div>
    """, unsafe_allow_html=True)

# View All Dramas Page
elif page == "View All Dramas":
    st.markdown("<h2 class='page-header'>All Pakistani Dramas</h2>", unsafe_allow_html=True)
    dramas = get_all_dramas()
    if dramas:
        # Sort options in a nice select box
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        sort_option = st.selectbox(
            "Sort by:",
            ["Title (A-Z)", "Title (Z-A)", "Year (Newest)", "Year (Oldest)", "Rating (Highest)", "Rating (Lowest)"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

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

        # Display dramas in a grid layout for larger screens
        st.markdown('<div class="drama-grid">', unsafe_allow_html=True)
        for drama in dramas:
            display_drama_card(drama)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📺</div>
            <h3>No dramas found</h3>
            <p>The database is currently empty. Please add some dramas first.</p>
        </div>
        """, unsafe_allow_html=True)

# Browse by Tags Page
elif page == "Browse by Tags":
    st.markdown("<h2 class='page-header'>Browse Dramas by Tags</h2>", unsafe_allow_html=True)

    # Get all available tags
    all_tags = get_all_tags()

    if all_tags:
        # Display tag cloud
        st.markdown('<div class="tag-cloud">', unsafe_allow_html=True)
        st.markdown('<h3 class="tag-cloud-title">Select a tag to browse dramas</h3>', unsafe_allow_html=True)

        # Check if a tag was selected from query params
        selected_tag = None
        if "tag" in query_params:
            selected_tag = query_params["tag"][0]

        # Create tag cloud with all tags
        tags_html = ""
        for tag in all_tags:
            tag_class = "tag tag-active" if selected_tag == tag else "tag"
            tags_html += f'<a href="?tag={tag}" target="_self"><span class="{tag_class}">{tag}</span></a>'

        st.markdown(tags_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # If a tag is selected, show dramas with that tag
        if selected_tag:
            st.markdown(f"<h3 class='section-header'>Dramas tagged with '{selected_tag}'</h3>", unsafe_allow_html=True)
            tagged_dramas = get_dramas_by_tag(selected_tag)

            if tagged_dramas:
                for drama in tagged_dramas:
                    display_drama_card(drama)
            else:
                st.info(f"No dramas found with the tag '{selected_tag}'.")
        else:
            # If no tag is selected, show a message
            st.markdown("""
            <div class="info-card">
                <h3>How to use tags</h3>
                <p>Click on any tag above to see dramas associated with that tag.</p>
                <p>Tags help you discover dramas by:</p>
                <ul>
                    <li>Era (80s, 90s, 2000s, etc.)</li>
                    <li>Genre (Romance, Family Drama, Comedy, etc.)</li>
                    <li>Channel (PTV, Hum TV, ARY Digital, etc.)</li>
                    <li>Special categories (Award-Winning, Classic, etc.)</li>
                </ul>
                <p>You can also click on tags shown on individual drama cards to find similar content.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No tags found in the database. Please add some dramas with tags first.")

# Add New Drama Page
elif page == "Add New Drama":
    st.markdown("<h2 class='page-header'>Add New Drama</h2>", unsafe_allow_html=True)
    from backend.database import add_drama
    import uuid
    import os
    from datetime import datetime

    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    with st.form("add_drama_form"):
        st.markdown("<h3 class='form-header'>Drama Details</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title", max_chars=255)
            director = st.text_input("Director", max_chars=255)
            year = st.number_input("Year", min_value=1950, max_value=2023, value=2020)
            channel = st.text_input("Channel", max_chars=100)
        with col2:
            episodes = st.number_input("Number of Episodes", min_value=1, value=20)
            rating = st.slider("Rating", min_value=1.0, max_value=10.0, value=8.0, step=0.1)
            # Add image upload feature
            uploaded_file = st.file_uploader("Upload Drama Poster", type=["jpg", "jpeg", "png"])

        # Add tags input
        all_tags = get_all_tags()
        suggested_tags = ["Family Drama", "Romance", "Comedy", "Thriller", "Mystery", "Social Issues",
                          "PTV", "Hum TV", "ARY Digital", "Geo TV", "Award-Winning", "Classic",
                          "80s", "90s", "2000s", "2010s", "2020s"]

        # Combine existing tags with suggested tags, remove duplicates
        tag_options = list(set(all_tags + suggested_tags))
        tag_options.sort()

        selected_tags = st.multiselect(
            "Select Tags (or create new ones by typing)",
            options=tag_options,
            default=[],
            help="Choose existing tags or create new ones"
        )

        description = st.text_area("Description", height=150)
        submitted = st.form_submit_button("Add Drama")

        if submitted:
            if not title or not director:
                st.error("Title and Director are required fields.")
            else:
                # Handle image upload and storage
                # Define the specific path for storing images
                images_dir = r"C:\DramaApp_IR\backend\images"
                os.makedirs(images_dir, exist_ok=True)
                if uploaded_file is not None:
                    # Generate a unique filename for the image
                    file_extension = uploaded_file.name.split(".")[-1]
                    unique_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
                    image_path = os.path.join(images_dir, unique_filename)
                    # Save the uploaded file
                    with open(image_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"Image uploaded successfully: {unique_filename}")
                else:
                    # Use a default placeholder image if no image is uploaded
                    unique_filename = "placeholder.jpg"
                    image_path = os.path.join(images_dir, unique_filename)
                    # Create the placeholder image if it doesn't exist
                    if not os.path.exists(image_path):
                        # Create a simple placeholder image
                        from PIL import Image, ImageDraw, ImageFont

                        img = Image.new('RGB', (300, 450), color=(200, 200, 200))
                        d = ImageDraw.Draw(img)
                        d.text((100, 225), "No Image", fill=(100, 100, 100))
                        img.save(image_path)

                # Store the full path in the database
                drama_id = add_drama(title, director, year, channel, episodes, rating, description, image_path,
                                     selected_tags)
                if drama_id:
                    st.success(f"Drama '{title}' added successfully with ID: {drama_id}")
                    st.balloons()
                    # Display the added drama with its image
                    st.markdown("<h3>Drama Added:</h3>", unsafe_allow_html=True)
                    st.markdown('<div class="drama-card">', unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        try:
                            img = Image.open(image_path)
                            st.image(img, width=200)
                        except Exception as e:
                            st.error(f"Error displaying image: {e}")
                            st.image("https://via.placeholder.com/200x300?text=No+Image", width=200)
                    with col2:
                        st.markdown(f"<h3 class='drama-title'>{title} ({year})</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p class='drama-info'><strong>Director:</strong> {director}</p>",
                                    unsafe_allow_html=True)
                        st.markdown(f"<p class='drama-info'><strong>Channel:</strong> {channel}</p>",
                                    unsafe_allow_html=True)
                        st.markdown(f"<p class='drama-info'><strong>Episodes:</strong> {episodes}</p>",
                                    unsafe_allow_html=True)
                        st.markdown(f"<p class='drama-rating'><strong>Rating:</strong> {rating}/10</p>",
                                    unsafe_allow_html=True)

                        # Display tags
                        if selected_tags:
                            tags_html = '<div class="drama-tags">'
                            for tag in selected_tags:
                                tags_html += f'<span class="tag">{tag}</span>'
                            tags_html += '</div>'
                            st.markdown(tags_html, unsafe_allow_html=True)

                        st.markdown(f"<p class='drama-description'>{description}</p>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("Failed to add drama. Please check your inputs and try again.")

    st.markdown('</div>', unsafe_allow_html=True)

# Search Dramas Page
elif page == "Search Dramas":
    st.markdown("<h2 class='page-header'>Search Pakistani Dramas</h2>", unsafe_allow_html=True)
    # Explanation of fuzzy search
    with st.expander("About Fuzzy Search"):
        st.markdown("""
        <div class="info-card">
            <h3>How Our Fuzzy Search Works</h3>
            <p>
                This search engine uses <strong>Levenshtein Edit Distance</strong> to find dramas even when the search term is misspelled.
            </p>
            <h4>What is Levenshtein Edit Distance?</h4>
            <p>
                The Levenshtein distance is a measure of the difference between two strings. It represents the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one string into another.
            </p>
            <h4>Why is this useful for Pakistani dramas?</h4>
            <p>
                Many Pakistani dramas have Urdu titles written in English, which can be spelled in different ways. For example, "Andhera Ujala" might be typed as "Andera Ujhala" or "Undera Ujala". Our fuzzy search will find the correct drama regardless of these variations.
            </p>
            <h4>How to use:</h4>
            <ol>
                <li>Enter a drama title or director name in the search box</li>
                <li>Adjust the fuzzy matching threshold if needed (lower values = more matches)</li>
                <li>Click Search</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("Enter drama title or director name")
    with col2:
        fuzzy_threshold = st.slider("Fuzzy Match Threshold", 0.0, 1.0, 0.3, 0.1,
                                    help="Lower values will match more variations (0.0-1.0)")
    search_button = st.button("Search", key="search_button")
    st.markdown('</div>', unsafe_allow_html=True)

    if search_term and search_button:
        dramas = search_dramas(search_term, fuzzy_threshold)
        if dramas:
            st.markdown(f"<h3 class='results-header'>Found {len(dramas)} results for '{search_term}'</h3>",
                        unsafe_allow_html=True)
            # If using fuzzy matching, show the Levenshtein distance for each match
            if fuzzy_threshold < 1.0:
                st.markdown("<h4 class='match-header'>Match Details</h4>", unsafe_allow_html=True)
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
                st.markdown('<div class="match-details-table">', unsafe_allow_html=True)
                st.table(match_details)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="search-results">', unsafe_allow_html=True)
            for drama in dramas:
                display_drama_card(drama)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="empty-state">
                <div class="empty-icon">🔍</div>
                <h3>No results found</h3>
                <p>No dramas found matching '{search_term}'.</p>
                <p>Try a different search term or adjust the fuzzy matching threshold.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="search-placeholder">
            <div class="search-icon">🔍</div>
            <h3>Search for Pakistani Dramas</h3>
            <p>Enter a drama title or director name to search the database.</p>
            <p class="search-tip">Our fuzzy search will find matches even if you misspell the title!</p>
            <div class="search-examples">
                <p>Examples:</p>
                <ul>
                    <li>Try searching for "Andera Ujala" instead of "Andhera Ujala"</li>
                    <li>Or "Zindgi Gulzar" instead of "Zindagi Gulzar Hai"</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""<footer class="footer">
    <div class="footer-content">
        <div class="footer-section">
            <h4>About</h4>
            <p>Pakistani Drama Database is a comprehensive collection of TV dramas from Pakistan's rich television history.</p>
        </div>
        <div class="footer-section">
            <h4>Features</h4>
            <ul>
                <li>Browse dramas</li>
                <li>Fuzzy search</li>
                <li>Add new dramas</li>
                <li>Browse by tags</li>
            </ul>
        </div>
        <div class="footer-section">
            <h4>Technology</h4>
            <ul>
                <li>Streamlit</li>
                <li>PostgreSQL</li>
                <li>Levenshtein Algorithm</li>
            </ul>
        </div>
    </div>
    <div class="footer-bottom">
        <p>Pakistani Drama Database © 2023 | Created with ❤️ | Featuring Levenshtein Edit Distance for fuzzy search</p>
    </div>
</footer>""", unsafe_allow_html=True)

