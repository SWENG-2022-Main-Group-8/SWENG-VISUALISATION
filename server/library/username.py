import json
import requests

# username = input("Enter username: ")

def re_to_json(username):
    try:
        url = "https://api.github.com/users/{}".format(username)
        response = requests.get(url)
        print(json.loads(response.text))
        return json.loads(response.text)
    except:
        print("User could not be found")
        return '{}'