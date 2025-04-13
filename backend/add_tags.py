import psycopg2
import os
import sys
import random

# Add the current directory to the path to allow absolute imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from postgres_database import get_connection


def add_tags_column():
    """Add tags column to the existing dramas table and populate with data"""
    conn = get_connection()
    if not conn:
        print("Failed to connect to the database")
        return

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
            print("Tags column added successfully")
        else:
            print("Tags column already exists")

        # Update existing dramas with tags
        print("Updating dramas with tags...")
        cursor.execute("SELECT id, title, year, channel, rating FROM dramas")
        dramas = cursor.fetchall()

        for drama in dramas:
            drama_id = drama[0]
            title = drama[1]
            year = drama[2]
            channel = drama[3]
            rating = drama[4]

            # Initialize tags list
            tags = []

            # Add era tags based on year
            if year and year < 1990:
                tags.append("80s")
            elif year and year < 2000:
                tags.append("90s")
            elif year and year < 2010:
                tags.append("2000s")
            elif year and year < 2020:
                tags.append("2010s")
            else:
                tags.append("2020s")

            # Add Classic tag for older dramas
            if year and year < 2000:
                tags.append("Classic")

            # Add channel tag if available
            if channel:
                channel_upper = channel.upper()
                if "PTV" in channel_upper:
                    tags.append("PTV")
                elif "GEO" in channel_upper:
                    tags.append("Geo TV")
                elif "ARY" in channel_upper:
                    tags.append("ARY Digital")
                elif "HUM" in channel_upper:
                    tags.append("Hum TV")
                elif "A-PLUS" in channel_upper or "APLUS" in channel_upper:
                    tags.append("A-Plus")
                elif "EXPRESS" in channel_upper:
                    tags.append("Express")

            # Add genre tags based on title or random assignment
            title_lower = title.lower() if title else ""
            if "love" in title_lower or "pyar" in title_lower or "ishq" in title_lower:
                tags.append("Romance")
            elif "family" in title_lower or "ghar" in title_lower:
                tags.append("Family Drama")
            elif "mystery" in title_lower or "raaz" in title_lower:
                tags.append("Mystery")
            else:
                # Add a random genre tag
                genres = ["Family Drama", "Romance", "Comedy", "Thriller", "Mystery", "Social Issues"]
                random_genre = random.choice(genres)
                tags.append(random_genre)

            # Add "Award-Winning" tag to high-rated dramas (rating > 8.5)
            if rating and rating > 8.5:
                tags.append("Award-Winning")

            # Update the drama with tags
            cursor.execute("UPDATE dramas SET tags = %s WHERE id = %s", (tags, drama_id))
            print(f"Updated drama '{title}' with tags: {tags}")

        conn.commit()
        print("Successfully added and populated tags column!")

    except Exception as e:
        conn.rollback()
        print(f"Error adding tags column: {e}")
    finally:
        cursor.close()
        conn.close()


def add_tag_functions():
    """Add functions to search and filter by tags"""
    conn = get_connection()
    if not conn:
        print("Failed to connect to the database")
        return

    try:
        cursor = conn.cursor()

        # Add function to get all unique tags
        print("Adding get_all_tags function...")
        cursor.execute('''
            CREATE OR REPLACE FUNCTION get_all_tags()
            RETURNS TABLE (tag_name TEXT) AS $$
            BEGIN
                RETURN QUERY
                SELECT DISTINCT unnest(tags) as tag
                FROM dramas
                WHERE tags IS NOT NULL
                ORDER BY tag;
            END;
            $$ LANGUAGE plpgsql;
        ''')

        # Add function to get dramas by tag
        print("Adding get_dramas_by_tag function...")
        cursor.execute('''
            CREATE OR REPLACE FUNCTION get_dramas_by_tag(tag_name TEXT)
            RETURNS TABLE (
                id INTEGER,
                title VARCHAR,
                director VARCHAR,
                year INTEGER,
                channel VARCHAR,
                episodes INTEGER,
                rating FLOAT,
                description TEXT,
                image_path VARCHAR,
                tags TEXT[]
            ) AS $$
            BEGIN
                RETURN QUERY
                SELECT *
                FROM dramas
                WHERE tags @> ARRAY[tag_name]
                ORDER BY title;
            END;
            $$ LANGUAGE plpgsql;
        ''')

        conn.commit()
        print("Successfully added database functions!")

    except Exception as e:
        conn.rollback()
        print(f"Error adding database functions: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # Add tags column and populate with data
    add_tags_column()

    # Add database functions for tags
    add_tag_functions()

    print("Database modification complete!")
