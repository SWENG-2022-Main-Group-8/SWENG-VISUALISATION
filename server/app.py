from flask import Flask, request
import backEnd
import json

app =  Flask(__name__)


@app.route("/username", methods=["GET", "POST"])
def user():
    print("message recieved!")
    #if request.method == "GET":
    #    data = backEnd.re_to_json()
    #    data1 =  data,200,{"ContentType":"application/json"}
    #    with open("users.json", "r") as f:
    #        data = json.load(f)
    #        data.append({
    #            "username": "user4",
    #            "pets": ["hamster"]
    #        })
    #        return Flask.jsonify(data)

    if request.method == "POST":
        print("post recieved!")
        data = request.get_json()
        username = data['data']
        print(username)
        data = backEnd.re_to_json(username)
        return Flask.Response(response=(data,200,{"ContentType":"application/json"}), status=201)

if __name__ == "__main__":
    app.run(debug=True)