import requests
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to fetch and process news data
def fetch_news(query):
    api_key = '2fb64be320a6418ca18285ec3a48c032'
    url = f'https://newsapi.org/v2/everything?q={query}&sortBy=popularity&apiKey={api_key}&language=en'
    response = requests.get(url)
    print(response.json())
    return response.json()

# Route to display the homepage with the search bar
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the search form submission
@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('query')
    if not search_query:
        return render_template('index.html', error="Please enter a search query.")
    
    data = fetch_news(search_query)
    articles = data.get('articles', [])
    
    return render_template('results.html', query=search_query, articles=articles)

# Start the Flask web server
if __name__ == '__main__':
    app.run(debug=True)
