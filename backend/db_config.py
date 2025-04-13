import os

# Check if running on Streamlit Cloud
is_streamlit_cloud = os.environ.get('IS_STREAMLIT_CLOUD', False)

if is_streamlit_cloud:
    # Use SQLite for Streamlit Cloud deployment
    DB_TYPE = 'sqlite'
    DB_PATH = 'dramas.db'
else:
    # Use PostgreSQL for local development
    DB_TYPE = 'postgresql'
    DB_HOST = 'localhost'
    DB_NAME = 'drama_db'
    DB_USER = 'ahmad'
    DB_PASSWORD = 'your_password'
