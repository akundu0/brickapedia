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
                "piece_count": set_data.get('num_parts', 'N/A'),
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

"""

@app.route('/api/get_set_parts', methods=['GET'])
def get_set_parts():
    set_id = request.args.get('set_id', '75192-1')  # Default set
    url = f"https://rebrickable.com/api/v3/lego/sets/{set_id}/parts/"
    headers = {"Authorization": f"key {API_KEY}"}

    all_parts = []  # Store all parts
    part_numbers = []  # Store part numbers only
    # colors = []

    while url:  # Handle pagination
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            all_parts.extend(data["results"])  # Add all parts
            part_numbers.extend([part["part"]["part_num"] for part in data["results"]])  # Store part numbers
            # colors.extend([])
            url = data.get("next")  # Get next page if exists
        else:
            return jsonify({"error": f"Request failed with status code {response.status_code}"}), response.status_code

    return jsonify({"set_id": set_id, "parts": all_parts, "part_numbers": part_numbers})
"""
# duplicate function using parameters:
# input: set_id, output: parts
def get_set_parts(set_id="75192-1"):
    url = f"https://rebrickable.com/api/v3/lego/sets/{set_id}/parts/"
    headers = {"Authorization": f"key {API_KEY}"}

    all_parts = []  # Store all parts
    part_numbers = []  # Store part numbers only
    # colors = []

    while url:  # Handle pagination
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            all_parts.extend(data["results"])  # Add all parts
            part_numbers.extend([part["part"]["part_num"] for part in data["results"]])  # Store part numbers
            # colors.extend([])
            url = data.get("next")  # Get next page if exists
        else:
            return jsonify({"error": f"Request failed with status code {response.status_code}"}), response.status_code

    return part_numbers
"""

@app.route('/api/get_sets_with_part', methods=['GET'])
def get_sets_with_part():
    part_num = request.args.get('part_num')  # Get part number from query parameter
    color_id = request.args.get('color_id')  # Get color ID from query parameter
    print("Received request for part:", part_num) 
    print("Received request for color:", color_id) 
    
    if not part_num or not color_id:
        return jsonify({"error": "Missing part number or color id"}), 400  # Return error if missing parameters

    # Correct URL with part_num and color_id
    url = f"https://rebrickable.com/api/v3/lego/parts/{part_num}/colors/{color_id}/sets/"
    headers = {"Authorization": f"key {API_KEY}"}

    all_sets = []  # Store all sets

    print(f"Fetching sets for part number: {part_num} and color: {color_id}")
    print(f"API Request URL: {url}")  # Debugging

    while url:  # Handle pagination
        response = requests.get(url, headers=headers)
        
        # Print full response for debugging
        print("Response Status Code:", response.status_code)
        print("Full API Response:", response.text)  # Debugging

        if response.status_code == 200:
            data = response.json()
            # Extend all_sets with the 'results' from the API response
            all_sets.extend(data.get("results", []))  # Add sets from response
            url = data.get("next")  # Check for next page
        else:
            return jsonify({"error": f"Request failed with status code {response.status_code}"}), response.status_code

    # Return the list of all sets for the given part number and color
    return jsonify({"part_num": part_num, "color_id": color_id, "sets": all_sets})
"""
# Duplicate function with parameters
# input: part + color, output: sets with part
def get_sets_with_part(part_num="3005", color_id="1"):
    print("Received request for part:", part_num) 
    print("Received request for color:", color_id) 
    
    if not part_num or not color_id:
        return jsonify({"error": "Missing part number or color id"}), 400  # Return error if missing parameters

    # Correct URL with part_num and color_id
    url = f"https://rebrickable.com/api/v3/lego/parts/{part_num}/colors/{color_id}/sets/"
    headers = {"Authorization": f"key {API_KEY}"}

    all_sets = []  # Store all sets

    print(f"Fetching sets for part number: {part_num} and color: {color_id}")
    print(f"API Request URL: {url}")  # Debugging

    while url:  # Handle pagination
        response = requests.get(url, headers=headers)
        
        # Print full response for debugging
        print("Response Status Code:", response.status_code)
        # print("Full API Response:", response.text)  # Debugging

        if response.status_code == 200:
            data = response.json()
            # Extend all_sets with the 'results' from the API response
            all_sets.extend(data.get("results", []))  # Add sets from response
            url = data.get("next")  # Check for next page
        else:
            return None

    # Return the list of all sets for the given part number and color
    return all_sets

@app.route('/api/get_sets_with_parts', methods=['GET'])
def get_sets_with_parts():
    set_id = request.args.get('set_id', '75192-1')  # Get set_id from query parameters
    color_id = request.args.get('color_id', 1)
    if (not set_id) or (not color_id):
        return jsonify({"error": "Missing set_id"}), 400

    # URL to fetch parts for the set
    url = f"https://rebrickable.com/api/v3/lego/sets/{set_id}/parts/"
    headers = {"Authorization": f"key {API_KEY}"}

    # Get the list of parts in the set
    response = requests.get(url, headers=headers)
    
    # Debugging: check if response is successful
    print("Response Status Code:", response.status_code)
    print("Full API Response:", response.text)

    if response.status_code != 200:
        return jsonify({"error": f"Request failed with status code {response.status_code}"}), response.status_code
    
    # Parse the parts data
    parts_data = response.json()
    part_numbers = [part['part']['part_num'] for part in parts_data['results']]

    # Now, for each part number, search for sets containing it
    all_sets = {}

    for part_num in part_numbers:
        part_url = f"https://rebrickable.com/api/v3/lego/parts/{part_num}/colors/{color_id}/sets/"
        part_response = requests.get(part_url, headers=headers)

        # Debugging: check if response for part is successful
        print(f"Fetching sets for part: {part_num}")
        print("Response Status Code:", part_response.status_code)

        if part_response.status_code == 200:
            part_sets_data = part_response.json()

            # Use a while loop to handle pagination for sets associated with this part
            while part_sets_data.get('next'):
                # Add sets from the current page
                for set_info in part_sets_data['results']:
                    all_sets[set_info['set_num']] = set_info  # Dictionary ensures uniqueness

                # Get the next page of results
                part_url = part_sets_data['next']  # 'next' contains the URL for the next page
                part_response = requests.get(part_url, headers=headers)
                part_sets_data = part_response.json()  # Get data from the next page

            # Add the remaining sets from the last page
            for set_info in part_sets_data['results']:
                all_sets[set_info['set_num']] = set_info  # Dictionary ensures uniqueness
        else:
            print(f"Failed to fetch sets for part {part_num}")

    # Convert dictionary values to a list for the final result
    unique_sets = list(all_sets.values())

    return jsonify({"set_id": set_id, "sets": unique_sets})


def get_set_dupe(set_id):
    print("Fetching set information...")

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
                "piece_count": set_data.get('num_parts', 'N/A'),
                "price": set_data.get('price', 'N/A'),
                "set_img_url": set_data.get('set_img_url', '')
            }
            print("Set Info (JSON):", set_info)

            # Return the data to the template (as JSON or render the HTML with the data)
            return set_info
        else:
            # Handle non-200 responses (error codes)
            return None

    except requests.exceptions.RequestException as e:
        # Handle network-related issues
        return jsonify({"error": str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search():
    input_set = request.args.get('set_id')
    parts = get_set_parts(input_set)
    count = 0
    output = dict()

    for part in parts:
        sets = get_sets_with_part(part_num=part)
        if count >= 11:
               break
        for set in sets:
           output[count] = get_set_dupe(set["set_num"])
           # append and make list of all sets with parts in the given set
           # dictionary to handle duplicates
           count += 1
           if count >= 11:
               break
    print("Sets (JSON): ", output)
    return render_template("results.html", output=output)
# For testing purposes, print the current working directory
import os
print("Current working directory:", os.getcwd())

if __name__ == '__main__':
    app.run(debug=True)

# test set: '75192-1'