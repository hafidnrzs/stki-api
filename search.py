import pandas as pd
from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os
import shutil

# Define the schema for the index
schema = Schema(id=ID(stored=True), title=TEXT(stored=True), content=TEXT(stored=True))

# Remove all files in the index directory except README
index_dir = 'indexdir'
if os.path.exists(index_dir):
    for filename in os.listdir(index_dir):
        if filename != 'README.md':
            file_path = os.path.join(index_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
else:
    os.mkdir(index_dir)

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
    for doc_id, title, content in documents:
        writer.add_document(id=doc_id, title=title, content=content)
    writer.commit()

def index_csv(file_path):
    df = pd.read_csv(file_path)
    df = df.head(1000) # Limit to 1000 documents for testing
    documents = [(str(row['id']), row['title'], row['content']) for _, row in df.iterrows()]
    add_documents(documents)

def search_documents(query_string, csv_file_path):
    with ix.searcher() as searcher:
        query = QueryParser('content', ix.schema).parse(query_string)
        results = searcher.search(query)
        result_ids = [result['id'] for result in results]

    # Load the CSV file to match the ids
    df = pd.read_csv(csv_file_path)
    matched_rows = df[df['id'].astype(str).isin(result_ids)]

    return matched_rows.to_dict(orient='records')