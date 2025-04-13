# Pakistani Drama Database with Fuzzy Search

A web application for browsing and searching Pakistani TV dramas, featuring fuzzy search capabilities using Levenshtein Edit Distance.


## Features

![image](https://github.com/user-attachments/assets/db8661a2-2adc-4e2a-8805-e78bdd50b974)

- Browse a collection of Pakistani dramas
- Search for dramas by title or director
![image](https://github.com/user-attachments/assets/bde59dec-4183-490e-a411-25ec32510f72)

- Fuzzy search using Levenshtein Edit Distance to handle misspellings and variations in Urdu words written in English
![image](https://github.com/user-attachments/assets/c1996c79-e54c-4ba7-9352-ad9421f6f140)

- Add new dramas to the database
![image](https://github.com/user-attachments/assets/3d7061cc-1e56-40bf-8393-529838accd26)

- Sort and filter dramas by various criteria A-Z, Z-A, by year, by rating, oldest, newest
![image](https://github.com/user-attachments/assets/88756ef6-9d30-4f77-af68-cc8a4c9713f1)
 
- Every drama has it own tag and by clicking on tag you can view more dramas like that comedy, old, classic, award winning, 6 more
![image](https://github.com/user-attachments/assets/4a7b743b-6afc-4c17-b945-2477a95f8646)


## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: PostgreSQL, SQLite (the project has sqlite file you can use sqlite for hassle free db setup)
- **Search Algorithm**: Levenshtein Edit Distance for fuzzy matching

## Levenshtein Edit Distance

This application implements the Levenshtein Edit Distance algorithm to provide fuzzy search capabilities. This is particularly useful for Pakistani dramas because:

1. Many Pakistani dramas have Urdu titles written in English
2. Urdu words can be transliterated into English in multiple ways
3. Users might misspell or use different variations of the same title

For example, "Andhera Ujala" (اندھیرا اجالا) might be typed as "Andera Ujhala", "Undera Ujala", etc. The fuzzy search will still find the correct drama.

## Setup and Installation

### Prerequisites

- Python 3.7+
- PostgreSQL

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/pakistani-drama-database.git
   cd pakistani-drama-database
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database:
   ```
   psql -U postgres
   CREATE DATABASE drama_db;
   \q
   ```

4. Initialize the database with sample data:
   ```
   python -m backend.init_db
   ```

5. Run the application:
   ```
   streamlit run frontend/app.py
   ```

## Usage

1. **Browse Dramas**: Navigate to "View All Dramas" to see the complete collection
2. **Search**: Use the "Search Dramas" page to find dramas by title or director
   - Adjust the fuzzy matching threshold to control how strict the matching should be
   - Lower threshold values will match more variations but might include false positives
3. **Add New Drama**: Use the form to add new dramas to the database
