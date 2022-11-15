import json
import requests

def re_to_json(username):
  response = requests.get("https://api.github.com/users/{}".format(username))
  return json.loads((response.text))
