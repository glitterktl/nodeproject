import json
from pathlib import Path
from flask import Flask, request, render_template_string, jsonify
from flask import send_file
from estimation import estimation

app = Flask(__name__)
index_file = Path(__file__).resolve().parent.parent / "index.html"

def form_to_json(form):
    pickup = form.get("pickup", "").strip()
    dropoff = form.get("dropoff", "").strip()
    return {
        "origin": {"address": pickup},
        "destination": {"address": dropoff},
        "travelMode": "DRIVE",
    }
####################################################################
@app.route('/', methods=['GET'])
def index():
    return send_file(index_file)
#####################################################################
@app.route('/prepare_route', methods=['POST'])
def prepare_route():
    route_json = form_to_json(request.form)
    app.logger.info(
        "Prepared Google Routes request body (not sent to Google yet):\n%s",
        json.dumps(route_json, indent=2),
    )
    if not route_json["origin"]["address"] or not route_json["destination"]["address"]:
        return "Please enter both a pickup and a dropoff location.", 400

    return render_template_string(
            index_file.read_text(encoding="utf-8"),
            pickup=route_json["origin"]["address"],
            dropoff=route_json["destination"]["address"],
            message="Google Routes request body prepared. Check the server logs for details.")
#########################################################################
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
##################################################################################
if __name__ == '__main__':
    app.run(debug=True, port = 5000)
