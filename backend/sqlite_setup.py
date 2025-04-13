import os
import sys
import json
import random
import sqlite3

# Add the current directory to the path to allow absolute imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def create_sqlite_database():
    """Create a SQLite database with sample Pakistani dramas for Streamlit Cloud deployment"""
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    # Create images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # Connect to SQLite database (will create it if it doesn't exist)
    db_path = 'data/drama_db.sqlite'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()

        # Create dramas table
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

        # Check if we already have data
        cursor.execute("SELECT COUNT(*) FROM dramas")
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"Database already contains {count} dramas. Skipping initialization.")
            return db_path

        # Sample Pakistani dramas data
        dramas = [
            {
                'title': 'Humsafar',
                'director': 'Sarmad Khoosat',
                'year': 2011,
                'channel': 'Hum TV',
                'episodes': 23,
                'rating': 8.9,
                'description': 'Humsafar is a Pakistani television drama serial based on the novel of the same name written by Farhat Ishtiaq. It tells the story of a couple, Ashar and Khirad, who are forced to marry due to family circumstances.',
                'image_path': 'images/humsafar.jpg'
            },
            {
                'title': 'Zindagi Gulzar Hai',
                'director': 'Sultana Siddiqui',
                'year': 2012,
                'channel': 'Hum TV',
                'episodes': 26,
                'rating': 9.1,
                'description': 'Zindagi Gulzar Hai follows the story of Kashaf Murtaza, a strong-willed middle-class girl, and Zaroon Junaid, a rich and charming man. Despite their different backgrounds, they fall in love and navigate the challenges of marriage.',
                'image_path': 'images/zindagi_gulzar_hai.jpg'
            },
            {
                'title': 'Andhera Ujala',
                'director': 'Tariq Mairaj',
                'year': 1984,
                'channel': 'PTV',
                'episodes': 46,
                'rating': 8.7,
                'description': 'Andhera Ujala is a classic Pakistani crime drama that follows the story of police officers fighting against crime and corruption. It was one of the most popular dramas of its time.',
                'image_path': 'images/andhera_ujala.jpg'
            },
            {
                'title': 'Dhoop Kinare',
                'director': 'Sahira Kazmi',
                'year': 1987,
                'channel': 'PTV',
                'episodes': 13,
                'rating': 8.8,
                'description': 'Dhoop Kinare is a medical drama that revolves around the lives of doctors at a hospital. It tells the love story of Dr. Ahmer and Dr. Zoya, who have contrasting personalities.',
                'image_path': 'images/dhoop_kinare.jpg'
            },
            {
                'title': 'Diyar-e-Dil',
                'director': 'Haseeb Hassan',
                'year': 2015,
                'channel': 'Hum TV',
                'episodes': 33,
                'rating': 8.6,
                'description': 'Diyar-e-Dil is a family drama that spans three generations. It explores themes of love, sacrifice, and family values in a traditional Pashtun family.',
                'image_path': 'images/diyar_e_dil.jpg'
            },
            {
                'title': 'Tanhaiyan',
                'director': 'Shahzad Khalil',
                'year': 1986,
                'channel': 'PTV',
                'episodes': 13,
                'rating': 8.9,
                'description': 'Tanhaiyan follows the story of two sisters, Zara and Sanya, who face various challenges after the death of their parents. It is considered one of the classic Pakistani dramas.',
                'image_path': 'images/tanhaiyan.jpg'
            },
            {
                'title': 'Alif',
                'director': 'Haseeb Hassan',
                'year': 2019,
                'channel': 'Geo TV',
                'episodes': 24,
                'rating': 8.5,
                'description': 'Alif is a spiritual journey of a filmmaker and a calligrapher. It explores the connection between art, spirituality, and the search for meaning in life.',
                'image_path': 'images/alif.jpg'
            },
            {
                'title': 'Sadqay Tumhare',
                'director': 'Mohammed Ehteshamuddin',
                'year': 2014,
                'channel': 'Hum TV',
                'episodes': 28,
                'rating': 8.3,
                'description': 'Sadqay Tumhare is a romantic drama set in rural Pakistan in the 1970s. It tells the story of Shano and Khalil, who were engaged in childhood but face obstacles in their relationship as adults.',
                'image_path': 'images/sadqay_tumhare.jpg'
            },
            {
                'title': 'Yakeen Ka Safar',
                'director': 'Shahzad Kashmiri',
                'year': 2017,
                'channel': 'Hum TV',
                'episodes': 31,
                'rating': 8.7,
                'description': 'Yakeen Ka Safar follows the story of Dr. Zubia and Dr. Asfandyar, who both have troubled pasts. They find healing and love as they work together at a hospital in a remote area.',
                'image_path': 'images/yakeen_ka_safar.jpg'
            },
            {
                'title': 'Pyarey Afzal',
                'director': 'Nadeem Baig',
                'year': 2013,
                'channel': 'ARY Digital',
                'episodes': 33,
                'rating': 8.8,
                'description': 'Pyarey Afzal is a romantic drama about Afzal, a simple man from a small town who falls in love with Farah, an educated girl from a wealthy family. The story explores the challenges they face due to their different backgrounds.',
                'image_path': 'images/pyarey_afzal.jpg'
            },
            {
                'title': 'Dastaan',
                'director': 'Haissam Hussain',
                'year': 2010,
                'channel': 'Hum TV',
                'episodes': 23,
                'rating': 8.6,
                'description': 'Dastaan is based on the novel Bano by Razia Butt. It tells the story of Bano and Hassan, whose lives are torn apart by the partition of India in 1947.',
                'image_path': 'images/dastaan.jpg'
            },
            {
                'title': 'Shehr-e-Zaat',
                'director': 'Sarmad Khoosat',
                'year': 2012,
                'channel': 'Hum TV',
                'episodes': 13,
                'rating': 8.4,
                'description': 'Shehr-e-Zaat follows the spiritual journey of Falak, a beautiful and self-centered girl who learns about true love and spirituality after facing heartbreak.',
                'image_path': 'images/shehr_e_zaat.jpg'
            },
            {
                'title': 'Suno Chanda',
                'director': 'Aehsun Talish',
                'year': 2018,
                'channel': 'Hum TV',
                'episodes': 30,
                'rating': 8.2,
                'description': 'Suno Chanda is a romantic comedy about Arsal and Ajiya, cousins who are forced to marry but constantly bicker and plan to divorce after Ramadan.',
                'image_path': 'images/suno_chanda.jpg'
            },
            {
                'title': 'Aangan',
                'director': 'Mohammed Ehteshamuddin',
                'year': 2018,
                'channel': 'Hum TV',
                'episodes': 35,
                'rating': 7.9,
                'description': 'Aangan is set in pre-partition India and follows the story of a family over several decades, exploring themes of love, loss, and the impact of political changes on personal lives.',
                'image_path': 'images/aangan.jpg'
            },
            {
                'title': 'Zindagi Dhoop Tum Gulzar Chhaon',
                'director': 'Kashif Nisar',
                'year': 2016,
                'channel': 'PTV',
                'episodes': 24,
                'rating': 7.8,
                'description': 'This drama explores the complexities of relationships and the challenges faced by a middle-class family. It highlights the importance of understanding and compromise in relationships.',
                'image_path': 'images/zindagi_dhoop.jpg'
            }
        ]

        # Insert dramas into the database with tags
        for drama in dramas:
            # Generate tags for each drama
            tags = []

            # Add era tags based on year
            year = drama['year']
            if year < 1990:
                tags.append("80s")
            elif year < 2000:
                tags.append("90s")
            elif year < 2010:
                tags.append("2000s")
            elif year < 2020:
                tags.append("2010s")
            else:
                tags.append("2020s")

            # Add Classic tag for older dramas
            if year < 2000:
                tags.append("Classic")

            # Add channel tag if available
            channel = drama['channel']
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
            title_lower = drama['title'].lower()
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
            if drama['rating'] > 8.5:
                tags.append("Award-Winning")

            # Convert tags list to JSON string
            tags_json = json.dumps(tags)

            # Insert drama with tags
            cursor.execute('''
                INSERT INTO dramas (title, director, year, channel, episodes, rating, description, image_path, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                drama['title'],
                drama['director'],
                drama['year'],
                drama['channel'],
                drama['episodes'],
                drama['rating'],
                drama['description'],
                drama['image_path'],
                tags_json
            ))

        conn.commit()
        print(f"Successfully added {len(dramas)} dramas to the SQLite database")

    except Exception as e:
        conn.rollback()
        print(f"Error creating SQLite database: {e}")
    finally:
        cursor.close()
        conn.close()

    return db_path


def verify_database(db_path):
    """Verify the database was created correctly"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Check if the dramas table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dramas'")
        if not cursor.fetchone():
            print("Error: dramas table does not exist!")
            return False

        # Count the number of dramas
        cursor.execute("SELECT COUNT(*) FROM dramas")
        count = cursor.fetchone()[0]
        print(f"Number of dramas in the database: {count}")

        # Show a sample of dramas with their tags
        cursor.execute("SELECT id, title, director, year, tags FROM dramas LIMIT 5")
        rows = cursor.fetchall()

        print("\nSample dramas:")
        for row in rows:
            tags = json.loads(row['tags']) if row['tags'] else []
            print(f"ID: {row['id']}, Title: {row['title']}, Director: {row['director']}, Year: {row['year']}")
            print(f"Tags: {', '.join(tags)}")
            print("-" * 50)

        return True

    except Exception as e:
        print(f"Error verifying database: {e}")
        return False

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    db_path = create_sqlite_database()
    print(f"SQLite database created at: {db_path}")

    # Verify the database
    print("\nVerifying database...")
    if verify_database(db_path):
        print("Database verification successful!")
    else:
        print("Database verification failed!")

    print("Database initialization complete")
