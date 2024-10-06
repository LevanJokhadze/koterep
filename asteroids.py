

from flask import Flask, render_template, jsonify
import json
import requests
from datetime import datetime
from fake_useragent import UserAgent
import os
app = Flask(__name__)

# Initialize user agent object
ua = UserAgent()

# API Key
API_KEY = 'QMUV7eP7KoBV9bKGJnbL7QW4lHIM4ySkFjYCjwvX'

@app.route('/')
def index():
    today_date = datetime.today().strftime('%Y-%m-%d')

    # Use a random user-agent for the request header
    headers = {
        'User-Agent': ua.random
    }

    # Send the request with headers
    response = requests.get(
        f'https://api.nasa.gov/neo/rest/v1/feed?api_key={API_KEY}',
        headers=headers
    )
    data = response.json()

    asteroids = []
    for date, asteroids_data in data["near_earth_objects"].items():
        if date == today_date:
            for data in asteroids_data:
                asteroid_info = {
                    'id': data['id'],
                    'name': data['name'],
                    'is_hazardous': data.get('is_potentially_hazardous_asteroid', False),
                    'diameter_min': data.get("estimated_diameter", {}).get("meters", {}).get("estimated_diameter_min", 0),
                    'diameter_max': data.get("estimated_diameter", {}).get("meters", {}).get("estimated_diameter_max", 0),
                }
                asteroids.append(asteroid_info)

    return render_template('index.html', asteroids=asteroids)

@app.route('/asteroid/<asteroid_id>')
def asteroid(asteroid_id):
    headers = {
        'User-Agent': ua.random
    }
    
    # Fetch asteroid details
    response = requests.get(
        f'https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}?api_key={API_KEY}',
        headers=headers
    )
    data = response.json()
    
    close_approach_dates = [approach['close_approach_date'] for approach in data['close_approach_data']]
    
    return jsonify({
        'name': data['name'],
        'close_approach_dates': close_approach_dates
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

