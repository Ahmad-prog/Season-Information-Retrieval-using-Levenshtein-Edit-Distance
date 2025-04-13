import os
import sys

# Add the current directory to the path to allow absolute imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import get_connection, create_tables


def initialize_database():
    """Initialize the database with sample Pakistani dramas"""
    # First create the tables
    create_tables()

    # Connect to the database
    conn = get_connection()
    if not conn:
        print("Failed to connect to the database")
        return

    try:
        cursor = conn.cursor()

        # Check if we already have data
        cursor.execute("SELECT COUNT(*) FROM dramas")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"Database already contains {count} dramas. Skipping initialization.")
            return

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

        # Insert dramas into the database
        for drama in dramas:
            cursor.execute('''
                INSERT INTO dramas (title, director, year, channel, episodes, rating, description, image_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                drama['title'],
                drama['director'],
                drama['year'],
                drama['channel'],
                drama['episodes'],
                drama['rating'],
                drama['description'],
                drama['image_path']
            ))

        conn.commit()
        print(f"Successfully added {len(dramas)} dramas to the database")

    except Exception as e:
        conn.rollback()
        print(f"Error initializing database: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # Create images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # Initialize the database
    initialize_database()
    print("Database initialization complete")
