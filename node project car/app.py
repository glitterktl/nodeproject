import json
import os
from pathlib import Path
from flask import Flask, request, render_template_string, jsonify
import requests
from estimation import estimation
API_KEY = os.environ.get("GOOGLE_ROUTES_KEY")
URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

app = Flask(__name__)
index_file = Path(__file__).resolve().parent.parent / "index.html"
###################################################################
def form_to_json(form):
    #gets called third by prpare route
    pickup = form.get("pickup", "").strip()
    dropoff = form.get("dropoff", "").strip()
    print({
        "origin": {"address": pickup},
        "destination": {"address": dropoff},
        "travelMode": "DRIVE",
    })
    return {
        "origin": {"address": pickup},
        "destination": {"address": dropoff},
        "travelMode": "DRIVE",
    }


def parse_route_info(route_data):
    routes = route_data.get("routes", [])
    if not routes:
        return None

    route = routes[0]
    seconds = float(route["duration"].removesuffix("s"))
    meters = int(route["distanceMeters"])
    return {
        "ride_time_mins": round(seconds / 60, 1),
        "ride_distance": meters,
    }


####################################################################
@app.route('/', methods=['GET'])
def index():
    #first one yh
    return render_template_string(
        index_file.read_text(encoding="utf-8"),
        message="",
    )
#####################################################################
@app.route('/prepare_route', methods=['POST'])
#second one
def prepare_route():
    print(4)
    route_json = form_to_json(request.form)
    if not route_json["origin"]["address"] or not route_json["destination"]["address"]:
        return render_template_string(
            index_file.read_text(encoding="utf-8"),
            pickup=route_json["origin"]["address"],
            dropoff=route_json["destination"]["address"],
            message="Please enter both a pickup and a dropoff location.",
        ), 400

    return send_to_routesapi(route_json)
#########################################################################
@app.route('/estimate_price', methods=['POST'])
def estimate_price():
    print(5)
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

@app.route('/send_to_routesapi', methods=['POST'])
def send_to_routesapi(route_json=None):
    if route_json is None:
        route_json = form_to_json(request.form)

    pickup = route_json["origin"]["address"]
    dropoff = route_json["destination"]["address"]
    if not API_KEY:
        return render_template_string(
            index_file.read_text(encoding="utf-8"),
            pickup=pickup,
            dropoff=dropoff,
            message="Route lookup is unavailable because the API key is not configured.",
        ), 503

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters",
    }

    try:
        response = requests.post(URL, headers=headers, json=route_json, timeout=10)
    except requests.RequestException:
        app.logger.exception("Google Routes request failed")
        return render_template_string(
            index_file.read_text(encoding="utf-8"),
            pickup=pickup,
            dropoff=dropoff,
            message="Could not contact Google Routes. Please try again.",
        ), 502

    if response.status_code == 200:
        try:
            route_data = response.json()
            route_info = parse_route_info(route_data)
        except (KeyError, TypeError, ValueError):
            app.logger.exception("Google Routes returned an invalid response")
            return render_template_string(
                index_file.read_text(encoding="utf-8"),
                pickup=pickup,
                dropoff=dropoff,
                message="Google Routes returned an invalid response.",
            ), 502

        if route_info is None:
            message = "No route was found for those locations. Check the names and try again."
            status = 404
        else:
            message = (
                f"Route found: {route_info['ride_time_mins']} minutes, "
                f"{route_info['ride_distance']} meters."
            )
            status = 200

        app.logger.info("Google Routes result: %s", json.dumps(route_info))
        return render_template_string(
            index_file.read_text(encoding="utf-8"),
            pickup=pickup,
            dropoff=dropoff,
            message=message,
        ), status
    else:
        try:
            error_data = response.json().get("error", {})
        except ValueError:
            error_data = {}

        if response.status_code == 404 or error_data.get("status") == "NOT_FOUND":
            message = "No route was found for those locations. Check the names and try again."
            status = 404
        else:
            message = f"Google Routes could not check this trip: {error_data.get('message', 'Please try again later.')}"
            status = 502

        app.logger.error("Google Routes API error %s: %s", response.status_code, response.text)
        return render_template_string(
            index_file.read_text(encoding="utf-8"),
            pickup=pickup,
            dropoff=dropoff,
            message=message,
        ), status
    

##################################################################

@app.route('/get_route_info', methods=['POST'])
def get_route_info():
    route_data = request.get_json(silent=True)
    if not isinstance(route_data, dict):
        return jsonify({"error": "A Google Routes response is required."}), 400

    try:
        route_info = parse_route_info(route_data)
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Google Routes returned invalid route details."}), 502

    if route_info is None:
        return jsonify({"error": "No route found"}), 404
    return jsonify(route_info)

if __name__ == '__main__':
    app.run(debug=True, port=5001)