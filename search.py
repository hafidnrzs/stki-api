import pandas as pd
from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import shutil

# Load environment variables from .env file
load_dotenv()

# Define the schema
desired_schema = Schema(
    id=ID(stored=True, unique=True),
    title=TEXT(stored=True),
    content=TEXT(stored=True)
)

def clear_index(index_dir):
    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.makedirs(index_dir)

# Clear the index directory before re-indexing
index_dir = os.getenv('INDEX_DIR')
clear_index(index_dir)

# Create or open the index
try:
    ix = create_in(index_dir, desired_schema)
except EmptyIndexError:
    ix = open_dir(index_dir)

# Create PostgreSQL connection
db_url = os.getenv('DB_URL')
engine = create_engine(db_url)

def add_documents(documents):
    writer = ix.writer()
    for doc_id, title, content in documents:
        writer.add_document(id=doc_id, title=title, content=content)
    writer.commit()

def index_db():
    with engine.connect() as conn:
        df = pd.read_sql_query('SELECT * FROM news LIMIT 5000', conn)
    documents = [(str(row['id']), row['title'], row['content']) for _, row in df.iterrows()]
    add_documents(documents)

def search_documents(query_string, page=1, per_page=10):
    ix = open_dir(index_dir)
    offset = (page - 1) * per_page
    
    with ix.searcher() as searcher:
        query = QueryParser('content', ix.schema).parse(query_string)
        results = searcher.search(query, limit=None)
        total_results = len(results)
        result_ids = [result['id'] for result in results[offset:offset + per_page]]
    
    if not result_ids:
        return pd.DataFrame(), total_results
    
    # Load the PostgreSQL database to match the ids
    query = text('SELECT * FROM news WHERE id IN :ids')
    with engine.connect() as conn:
        news_data = pd.read_sql_query(query, conn, params={'ids': tuple(result_ids)})
    
    return news_data, total_results