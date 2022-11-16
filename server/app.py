from flask import Flask, request
import flask
from library import username as usernameAPI
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
        with open("server\OmaidQ.json", "r") as f:
            data = json.load(f)
            return flask.jsonify(data)
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        username = received_data['data']
        data = usernameAPI.re_to_json(username)
        return flask.Response(response=json.dumps(data), status=201)

if __name__ == "__main__":
    app.run(debug=True)

