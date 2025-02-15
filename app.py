import requests
from flask import Flask, render_template, request, jsonify


API_KEY = "Y90474b52a4291bd0d3ba0a85c7c9c323"
app = Flask(__name__)

@app.route('/api/get_set', methods=['GET'])

def get_set():
    set_id = request.args.get('set_id', '75192-1')
    url = f"https://rebrickable.com/api/v3/lego/sets/{set_id}/"
    headers = {"Authorization": f"key {API_KEY}"}
    
    response = requests.get(url, headers=headers)
    
    return jsonify(response.json())
