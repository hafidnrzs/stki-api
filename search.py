import pandas as pd
from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
import os

# Define the schema for the index
schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))

# Create an index directory if it doesn't exist
if not os.path.exists('indexdir'):
    os.mkdir('indexdir')

# Create or open the index
try:
    if not os.listdir('indexdir'):
        ix = create_in('indexdir', schema)
    else:
        ix = open_dir('indexdir')
except EmptyIndexError:
    ix = create_in('indexdir', schema)

def add_documents(documents):
    writer = ix.writer()
    for title, content in documents:
        writer.add_document(title=title, content=content)
    writer.commit()

def index_csv(file_path):
    df = pd.read_csv(file_path)
    df = df.fillna('')  # Replace NaN values with empty strings
    df = df.head(100)  # Limit to the first 100 rows
    documents = [(row['title'], row['content']) for _, row in df.iterrows()]
    add_documents(documents)

def search_documents(query_string):
    with ix.searcher() as searcher:
        query = QueryParser('content', ix.schema).parse(query_string)
        results = searcher.search(query)
        return [{'title': result['title'], 'content': result['content']} for result in results]