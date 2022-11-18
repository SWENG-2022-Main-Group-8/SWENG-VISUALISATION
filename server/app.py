from flask import Flask, request
import flask
from library import username as usernameAPI
from library import languageData as languagesAPI
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
        languages = languagesAPI.retrieveLanguages("OmaidQ")
        with open("OmaidQ.json", "r") as f:
            data = json.load(f)
            merge = dict(data.items() | languages.items())
            return flask.jsonify(merge)

    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        username = received_data['data']
        userInfo = usernameAPI.userInfo(username)
        languages = languagesAPI.retrieveLanguages(username)
        mergeOfDataAndLanguages = dict(userInfo.items() | languages.items())
        return flask.Response(response=json.dumps(mergeOfDataAndLanguages), status=201)

if __name__ == "__main__":
    app.run(debug=True)
