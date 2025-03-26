import requests
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, request
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.template_filter('format_time')
def format_time(date_str):
    try:
        # Parse the ISO format date string
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))  # Handle 'Z'
        now = datetime.now(pytz.UTC)
        diff = now - dt

        # Less than 1 hour
        if diff.total_seconds() < 3600:
            return "Less than 1 hour ago"

        # Between 1 and 24 hours
        hours = diff.total_seconds() / 3600
        if hours < 24:
            return f"{int(hours)} hrs ago"

        # More than 24 hours
        return dt.strftime("%b %d, %Y")

    except ValueError:
        return "Invalid date format"  # Or handle the error in a more appropriate way for your application


# Function to fetch and process news data
def fetch_news(query):
    api_key = os.getenv('api_key_newssapiorg')
    url = f'https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&searchin=title&apiKey={api_key}&language=en'
    response = requests.get(url)
    print(response.json())
    return response.json()

def get_paginated_articles(articles, page, per_page=15):
    start = (page - 1) * per_page
    end = start + per_page
    return articles[start:end]

# Route to display the homepage with the search bar
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the search form submission
@app.route('/search', methods=['POST', 'GET'])
def search():
    search_query = request.form.get('query') or request.args.get('query')
    page = request.args.get('page', 1, type=int)
    
    if not search_query:
        return render_template('index.html', error="Please enter a search query.")
    
    data = fetch_news(search_query)
    all_articles = data.get('articles', [])
    
    # Calculate pagination
    total_articles = len(all_articles)
    total_pages = (total_articles + 29) // 30  # ceiling division) 
    
    # Get articles for current page
    articles = get_paginated_articles(all_articles, page)
    
    return render_template('results.html', 
                         query=search_query, 
                         articles=articles,
                         current_page=page,
                         total_pages=total_pages)

# Start the Flask web server
if __name__ == '__main__':
    app.run(debug=True)
