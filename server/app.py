from flask import Flask

app =  Flask(__name__)

@app.route('/')
def index():
    return "Hello world!"

@app.route("/username")
def user():
    data = 
    return data,200,{"ContentType":"application/json"}

if __name__ == "__main__":
    app.run(debug=True)

