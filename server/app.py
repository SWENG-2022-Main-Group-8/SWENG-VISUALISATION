
from flask import Flask, request
import requests
import flask
from library import username as usernameAPI
from library import individualMap as mapAPI
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello world!"

@app.route('/username', methods=["GET", "POST"])
def users():
    print("users endpoint reached...")
    if request.method == "GET":
        with open("OmaidQ.json", "r") as f:
            data = json.load(f)
            return flask.jsonify(data)
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        username = received_data['data']
        data = usernameAPI.re_to_json(username)
        print("---------------------")
        coords = mapAPI.getLatLng(data.get("location"))
        data = mapAPI.mergeDictionary(data, coords)
        print(data)
        return flask.Response(response=json.dumps(data), status=201)

@app.route('/react', methods=["GET"])
def react():
    try:
        url = "https://api.github.com/repos/facebook/react/contributors?per_page=100"
        response =  requests.get(url)
        print(json.loads(response.text))
        return json.loads(response.text)

    except:
        print("Error")
        return '{}'

if __name__ == "__main__":
    app.run(debug=True)

#maps api key - AIzaSyCaN_NjULWKTMBVQYhQMCHoUIcJvg3fQUk