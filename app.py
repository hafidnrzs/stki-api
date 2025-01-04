from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from search import search_documents
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

db_url = os.getenv('DB_URL')

# Create PostgreSQL connection
engine = create_engine(db_url)

def get_news_data():
    with engine.connect() as conn:
        news_data = pd.read_sql_query('SELECT * FROM news', conn)
    return news_data

@app.route('/news', methods=['GET'])
def get_news():
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    
    # Get category from query parameters
    category = request.args.get('category', default=None, type=str)
    
    # Fetch news data
    news_data = get_news_data()
    
    # Filter by category if provided
    if category:
        news_data = news_data[news_data['category'] == category]
    
    # Paginate results
    total_results = len(news_data)
    paginated_data = news_data.iloc[start:end]
    
    return jsonify({
        'page': page,
        'per_page': per_page,
        'total': total_results,
        'news': paginated_data.to_dict(orient='records')
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)