import os
import sys
import json
import sqlite3
from pathlib import Path

# Define the database file path
DB_PATH = Path("data/drama_db.sqlite")

# Ensure the directory exists
os.makedirs(DB_PATH.parent, exist_ok=True)


def get_connection():
    """Create a connection to the SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON")
    # Return dictionary-like rows
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    """Create necessary tables if they don't exist"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Create dramas table with SQLite syntax
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dramas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    director TEXT,
                    year INTEGER,
                    channel TEXT,
                    episodes INTEGER,
                    rating REAL,
                    description TEXT,
                    image_path TEXT,
                    tags TEXT
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
                # Parse tags from JSON string
                tags = json.loads(row['tags']) if row['tags'] else []

                drama = {
                    'id': row['id'],
                    'title': row['title'],
                    'director': row['director'],
                    'year': row['year'],
                    'channel': row['channel'],
                    'episodes': row['episodes'],
                    'rating': row['rating'],
                    'description': row['description'],
                    'image_path': row['image_path'],
                    'tags': tags
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
            # Convert tags list to JSON string for SQLite storage
            tags_json = json.dumps(tags) if tags else None

            cursor.execute('''
                INSERT INTO dramas (title, director, year, channel, episodes, rating, description, image_path, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, director, year, channel, episodes, rating, description, image_path, tags_json))

            # Get the ID of the newly inserted drama
            drama_id = cursor.lastrowid
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
    Search for dramas by title or director
    Args:
        search_term (str): The search term to look for
        fuzzy_threshold (float): Threshold for fuzzy matching (0 to 1)
    Returns:
        list: List of matching drama dictionaries
    """
    conn = get_connection()
    matching_dramas = []
    if conn:
        try:
            cursor = conn.cursor()
            # Use SQLite's LIKE for basic pattern matching (case insensitive)
            search_pattern = f"%{search_term}%"
            cursor.execute('''
                SELECT * FROM dramas 
                WHERE title LIKE ? OR director LIKE ?
                ORDER BY title
            ''', (search_pattern, search_pattern))

            rows = cursor.fetchall()

            # Convert rows to drama dictionaries
            for row in rows:
                # Parse tags from JSON string
                tags = json.loads(row['tags']) if row['tags'] else []

                drama = {
                    'id': row['id'],
                    'title': row['title'],
                    'director': row['director'],
                    'year': row['year'],
                    'channel': row['channel'],
                    'episodes': row['episodes'],
                    'rating': row['rating'],
                    'description': row['description'],
                    'image_path': row['image_path'],
                    'tags': tags
                }
                matching_dramas.append(drama)

            # For fuzzy matching, you would need to implement the is_fuzzy_match function
            # and apply it to all dramas if no exact matches are found

        except Exception as e:
            print(f"Error searching dramas: {e}")
        finally:
            cursor.close()
            conn.close()
    return matching_dramas


def get_all_tags():
    """Get all unique tags from dramas"""
    conn = get_connection()
    all_tags = set()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT tags FROM dramas WHERE tags IS NOT NULL")
            rows = cursor.fetchall()

            # Extract tags from each drama
            for row in rows:
                tags_json = row['tags']
                if tags_json:
                    tags = json.loads(tags_json)
                    for tag in tags:
                        all_tags.add(tag)

            # Convert to sorted list
            tags_list = sorted(list(all_tags))
            return tags_list
        except Exception as e:
            print(f"Error retrieving all tags: {e}")
        finally:
            cursor.close()
            conn.close()
    return []


def get_dramas_by_tag(tag_name):
    """Get all dramas with a specific tag"""
    conn = get_connection()
    dramas = []
    if conn:
        try:
            cursor = conn.cursor()
            # SQLite doesn't have array operators, so we need to use JSON functions
            cursor.execute("SELECT * FROM dramas WHERE tags IS NOT NULL ORDER BY title")
            rows = cursor.fetchall()

            for row in rows:
                tags_json = row['tags']
                if tags_json:
                    tags = json.loads(tags_json)
                    if tag_name in tags:
                        drama = {
                            'id': row['id'],
                            'title': row['title'],
                            'director': row['director'],
                            'year': row['year'],
                            'channel': row['channel'],
                            'episodes': row['episodes'],
                            'rating': row['rating'],
                            'description': row['description'],
                            'image_path': row['image_path'],
                            'tags': tags
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
            # Convert tags list to JSON string
            tags_json = json.dumps(tags) if tags else None
            cursor.execute("UPDATE dramas SET tags = ? WHERE id = ?", (tags_json, drama_id))
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
            cursor.execute("SELECT * FROM dramas WHERE id = ?", (drama_id,))
            row = cursor.fetchone()
            if row:
                # Parse tags from JSON string
                tags = json.loads(row['tags']) if row['tags'] else []

                drama = {
                    'id': row['id'],
                    'title': row['title'],
                    'director': row['director'],
                    'year': row['year'],
                    'channel': row['channel'],
                    'episodes': row['episodes'],
                    'rating': row['rating'],
                    'description': row['description'],
                    'image_path': row['image_path'],
                    'tags': tags
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
            # Convert tags list to JSON string
            tags_json = json.dumps(tags) if tags is not None else None

            cursor.execute('''
                UPDATE dramas 
                SET title = ?, director = ?, year = ?, channel = ?,
                    episodes = ?, rating = ?, description = ?, image_path = ?, tags = ?
                WHERE id = ?
            ''', (title, director, year, channel, episodes, rating, description, image_path, tags_json, drama_id))

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
            cursor.execute("DELETE FROM dramas WHERE id = ?", (drama_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error deleting drama: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


# Initialize database tables when module is imported
create_tables()
