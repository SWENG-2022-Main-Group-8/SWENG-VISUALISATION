from flask import Flask, request
import backEnd as bk
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
        with open("users.json", "r") as f:
            data = json.load(f)
            data.append({
                "username": "user4",
                "pets": ["hamster"]
            })
            return Flask.jsonify(data)
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        username = received_data['data']
        data = bk.re_to_json(username)
        return Flask.Response(response=json.dumps(data), status=201)

if __name__ == "__main__":
    app.run(debug=True)

