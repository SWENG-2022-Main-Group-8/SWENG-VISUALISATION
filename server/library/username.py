import json
import requests

def userInfo(username):
    try:
        url = "https://api.github.com/users/{}".format(username)
        response = requests.get(url)
        return json.loads(response.text)
    except:
        print("User could not be found")
        return '{}'