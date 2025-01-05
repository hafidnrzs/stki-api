import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create PostgreSQL connection
db_url = os.getenv('DB_URL')
engine = create_engine(db_url)

def search_documents(query_string, page=1, per_page=10):
    offset = (page - 1) * per_page
    
    # Use PostgreSQL to search documents
    search_query = text("""
        SELECT *, COUNT(*) OVER() AS total_count
        FROM news
        WHERE content ILIKE :query_string
        ORDER BY id
        LIMIT :per_page OFFSET :offset
    """)
    
    with engine.connect() as conn:
        news_data = pd.read_sql_query(search_query, conn, params={
            'query_string': f'%{query_string}%',
            'per_page': per_page,
            'offset': offset
        })
    
    total_results = int(news_data['total_count'][0]) if not news_data.empty else 0
    news_data.drop(columns=['total_count'], inplace=True)
    
    return news_data, total_results