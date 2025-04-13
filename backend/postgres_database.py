import os
import sys

# Add the current directory to the path to allow absolute imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from levenshtein import is_fuzzy_match

# Check if running on Streamlit Cloud
is_streamlit_cloud = os.environ.get('IS_STREAMLIT_CLOUD', False)

def get_connection():
    """Establish a connection to the database (PostgreSQL or SQLite)"""
    if is_streamlit_cloud:
        # Use SQLite for Streamlit Cloud deployment
        import sqlite3
        try:
            # Create a data directory if it doesn't exist
            os.makedirs('data', exist_ok=True)
            conn = sqlite3.connect('data/drama_db.sqlite')
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"SQLite connection error: {e}")
            return None
    else:
        # Use PostgreSQL for local development
        import psycopg2
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="drama_db",  # Make sure this database exists in PostgreSQL
                user="ahmad",  # Replace with your PostgreSQL username
                password="#Ahmad1235$"  # Replace with your PostgreSQL password
            )
            return conn
        except Exception as e:
            print(f"PostgreSQL connection error: {e}")
            return None


def create_tables():
    """Create necessary tables if they don't exist"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Create dramas table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dramas (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    director VARCHAR(255),
                    year INTEGER,
                    channel VARCHAR(100),
                    episodes INTEGER,
                    rating FLOAT,
                    description TEXT,
                    image_path VARCHAR(255),
                    tags TEXT[]
                )
            ''')
            conn.commit()
            print("Tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()
            conn.close()


def get_all_dramas():
    """Retrieve all dramas from the database"""
    conn = get_connection()
    dramas = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dramas ORDER BY title")
            rows = cursor.fetchall()
            for row in rows:
                drama = {
                    'id': row[0],
                    'title': row[1],
                    'director': row[2],
                    'year': row[3],
                    'channel': row[4],
                    'episodes': row[5],
                    'rating': row[6],
                    'description': row[7],
                    'image_path': row[8],
                    'tags': row[9] if len(row) > 9 else []
                }
                dramas.append(drama)
        except Exception as e:
            print(f"Error retrieving dramas: {e}")
        finally:
            cursor.close()
            conn.close()
    return dramas


def add_drama(title, director, year, channel, episodes, rating, description, image_path, tags=None):
    """Add a new drama to the database"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if tags:
                cursor.execute('''
                    INSERT INTO dramas (title, director, year, channel, episodes, rating, description, image_path, tags)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                ''', (title, director, year, channel, episodes, rating, description, image_path, tags))
            else:
                cursor.execute('''
                    INSERT INTO dramas (title, director, year, channel, episodes, rating, description, image_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                ''', (title, director, year, channel, episodes, rating, description, image_path))
            drama_id = cursor.fetchone()[0]
            conn.commit()
            return drama_id
        except Exception as e:
            conn.rollback()
            print(f"Error adding drama: {e}")
            return None
        finally:
            cursor.close()
            conn.close()


def search_dramas(search_term, fuzzy_threshold=0.3):
    """
    Search for dramas by title or director with fuzzy matching support
    Args:
        search_term (str): The search term to look for
        fuzzy_threshold (float): Threshold for fuzzy matching (0 to 1)
    Returns:
        list: List of matching drama dictionaries
    """
    conn = get_connection()
    all_dramas = []
    matching_dramas = []
    if conn:
        try:
            cursor = conn.cursor()
            # First, get exact matches using SQL LIKE
            search_pattern = f"%{search_term}%"
            cursor.execute('''
                SELECT * FROM dramas 
                WHERE title ILIKE %s OR director ILIKE %s
                ORDER BY title
            ''', (search_pattern, search_pattern))
            rows = cursor.fetchall()
            # Convert rows to drama dictionaries
            for row in rows:
                drama = {
                    'id': row[0],
                    'title': row[1],
                    'director': row[2],
                    'year': row[3],
                    'channel': row[4],
                    'episodes': row[5],
                    'rating': row[6],
                    'description': row[7],
                    'image_path': row[8],
                    'tags': row[9] if len(row) > 9 else []
                }
                all_dramas.append(drama)
                matching_dramas.append(drama)  # Add exact matches

            # If we didn't find any exact matches, get all dramas for fuzzy matching
            if not matching_dramas:
                cursor.execute("SELECT * FROM dramas ORDER BY title")
                rows = cursor.fetchall()
                for row in rows:
                    drama = {
                        'id': row[0],
                        'title': row[1],
                        'director': row[2],
                        'year': row[3],
                        'channel': row[4],
                        'episodes': row[5],
                        'rating': row[6],
                        'description': row[7],
                        'image_path': row[8],
                        'tags': row[9] if len(row) > 9 else []
                    }
                    all_dramas.append(drama)

                # Apply fuzzy matching to find similar titles or directors
                for drama in all_dramas:
                    # Check if search term is similar to title
                    if is_fuzzy_match(search_term, drama['title'], fuzzy_threshold):
                        matching_dramas.append(drama)
                        continue
                    # Check if search term is similar to director
                    if is_fuzzy_match(search_term, drama['director'], fuzzy_threshold):
                        matching_dramas.append(drama)
                        continue
                    # Check if search term is similar to any word in the title
                    title_words = drama['title'].split()
                    for word in title_words:
                        if is_fuzzy_match(search_term, word, fuzzy_threshold):
                            matching_dramas.append(drama)
                            break

                # Remove duplicates (a drama might match multiple criteria)
                seen_ids = set()
                unique_matching_dramas = []
                for drama in matching_dramas:
                    if drama['id'] not in seen_ids:
                        seen_ids.add(drama['id'])
                        unique_matching_dramas.append(drama)
                matching_dramas = unique_matching_dramas
        except Exception as e:
            print(f"Error searching dramas: {e}")
        finally:
            cursor.close()
            conn.close()
    return matching_dramas


def add_tags_column():
    """Add tags column to dramas table if it doesn't exist"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Check if tags column already exists
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='dramas' AND column_name='tags'
            """)

            if not cursor.fetchone():
                # Add tags column to dramas table
                print("Adding tags column to dramas table...")
                cursor.execute("ALTER TABLE dramas ADD COLUMN tags TEXT[]")
                conn.commit()
                print("Tags column added successfully")
            else:
                print("Tags column already exists")
        except Exception as e:
            conn.rollback()
            print(f"Error adding tags column: {e}")
        finally:
            cursor.close()
            conn.close()


def get_all_tags():
    """Get all unique tags from dramas"""
    conn = get_connection()
    tags = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT unnest(tags) as tag
                FROM dramas
                WHERE tags IS NOT NULL
                ORDER BY tag
            """)
            tags = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error retrieving all tags: {e}")
        finally:
            cursor.close()
            conn.close()
    return tags


def get_dramas_by_tag(tag_name):
    """Get all dramas with a specific tag"""
    conn = get_connection()
    dramas = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM dramas
                WHERE tags @> ARRAY[%s]
                ORDER BY title
            """, (tag_name,))
            rows = cursor.fetchall()
            for row in rows:
                drama = {
                    'id': row[0],
                    'title': row[1],
                    'director': row[2],
                    'year': row[3],
                    'channel': row[4],
                    'episodes': row[5],
                    'rating': row[6],
                    'description': row[7],
                    'image_path': row[8],
                    'tags': row[9] if len(row) > 9 else []
                }
                dramas.append(drama)
        except Exception as e:
            print(f"Error retrieving dramas by tag: {e}")
        finally:
            cursor.close()
            conn.close()
    return dramas


def update_drama_tags(drama_id, tags):
    """Update tags for an existing drama"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE dramas SET tags = %s WHERE id = %s", (tags, drama_id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error updating drama tags: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


def get_drama_by_id(drama_id):
    """Get a drama by its ID"""
    conn = get_connection()
    drama = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dramas WHERE id = %s", (drama_id,))
            row = cursor.fetchone()
            if row:
                drama = {
                    'id': row[0],
                    'title': row[1],
                    'director': row[2],
                    'year': row[3],
                    'channel': row[4],
                    'episodes': row[5],
                    'rating': row[6],
                    'description': row[7],
                    'image_path': row[8],
                    'tags': row[9] if len(row) > 9 else []
                }
        except Exception as e:
            print(f"Error retrieving drama by ID: {e}")
        finally:
            cursor.close()
            conn.close()
    return drama


def update_drama(drama_id, title, director, year, channel, episodes, rating, description, image_path, tags=None):
    """Update an existing drama"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if tags is not None:
                cursor.execute('''
                    UPDATE dramas 
                    SET title = %s, director = %s, year = %s, channel = %s, 
                        episodes = %s, rating = %s, description = %s, image_path = %s, tags = %s
                    WHERE id = %s
                ''', (title, director, year, channel, episodes, rating, description, image_path, tags, drama_id))
            else:
                cursor.execute('''
                    UPDATE dramas 
                    SET title = %s, director = %s, year = %s, channel = %s, 
                        episodes = %s, rating = %s, description = %s, image_path = %s
                    WHERE id = %s
                ''', (title, director, year, channel, episodes, rating, description, image_path, drama_id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error updating drama: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


def delete_drama(drama_id):
    """Delete a drama from the database"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM dramas WHERE id = %s", (drama_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error deleting drama: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
