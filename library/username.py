import json
import requests

username = input("Enter username: ")
url = "https://api.github.com/users/{}".format(username)

def re_to_json():
    response = requests.get(url)
    print(json.loads(response.text))
    return json.loads(response.text)