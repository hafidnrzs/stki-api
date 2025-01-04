from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load dataset
data_file = 'data/news.csv'
news_data = pd.read_csv(data_file)

@app.route('/news', methods=['GET'])
def get_news():
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    
    # Get category from query parameters
    category = request.args.get('category', default=None, type=str)

    # Filter news data by category if provided
    if category:
        filtered_news = news_data[news_data['category'] == category]
    else:
        filtered_news = news_data

    paginated_news = filtered_news[start:end].to_dict(orient='records')
    
    return jsonify({
        'page': page,
        'per_page': per_page,
        'total': len(filtered_news),
        'news': paginated_news
    })

if __name__ == '__main__':
    app.run(debug=True)