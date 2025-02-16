import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env
API_KEY = os.getenv('API_KEY')

# Debugging: Check if API_KEY is loaded correctly
if not API_KEY:
    print("Error: API_KEY not loaded from .env")
else:
    print(f"API Key Loaded: {API_KEY}")

app = Flask(__name__, template_folder='templates/')

@app.route('/api/get_set', methods=['GET'])
def get_set():
    print("Fetching set information...")

    # Get 'set_id' from query parameters (default to '75192-1' if not provided)
    set_id = request.args.get('set_id', '75192-1')

    # Define the URL to call the Rebrickable API
    url = f"https://rebrickable.com/api/v3/lego/sets/{set_id}/"
    headers = {"Authorization": f"key {API_KEY}"}

    try:
        # Make the API request
        response = requests.get(url, headers=headers)

        print("API Response Text:", response.text)

        if response.status_code == 200:
            # Parse the JSON response
            set_data = response.json()
            print(set_data)

            # Prepare data to pass to the template
            set_info = {
                "name": set_data.get('name', 'N/A'),
                "set_id": set_data.get('set_num', 'N/A'),
                "year": set_data.get('year', 'N/A'),
                "piece_count": set_data.get('pieces', 'N/A'),
                "price": set_data.get('price', 'N/A'),
                "set_img_url": set_data.get('set_img_url', '')
            }
            print("Set Info (JSON):", set_info)

            # Return the data to the template (as JSON or render the HTML with the data)
            return render_template('results.html', set_info=set_info)
        else:
            # Handle non-200 responses (error codes)
            return jsonify({"error": f"Request failed with status code {response.status_code}"}), response.status_code

    except requests.exceptions.RequestException as e:
        # Handle network-related issues
        return jsonify({"error": str(e)}), 500

# Define the root route to pass `set_id` to the template
@app.route('/', methods=['GET'])
def home():
    # Get 'set_id' from query parameters (default to '75192-1')
    set_id = request.args.get('set_id', '75192-1')
    return render_template('results.html', set_id=set_id)

# For testing purposes, print the current working directory
import os
print("Current working directory:", os.getcwd())

if __name__ == '__main__':
    app.run(debug=True)
