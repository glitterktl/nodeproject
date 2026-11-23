from pathlib import Path

from flask import Flask, jsonify, request
from flask import send_file
from estimation import estimation

app = Flask(__name__)
index_file = Path(__file__).resolve().parent.parent / "index.html"

@app.route('/', methods=['GET'])
def index():
    return send_file(index_file)

@app.route('/estimate_price', methods=['POST'])
def estimate_price():
    data = request.get_json()
    ride_time = data.get('ride_time')
    ride_distance = data.get('ride_distance')
    isitrain = data.get('isitrain', False)
    traffic = data.get('traffic', 1)
    availability = data.get('availability', 1)

    # Create an instance of the estimation class
    estimator = estimation(data, ride_time, ride_distance, isitrain, traffic, availability)
    
    # Calculate the price estimation
    estimated_price = estimator.calculate_estimation()
    
    return jsonify({"estimated_price": estimated_price})

if __name__ == '__main__':
    app.run(debug=True, port = 5000)
