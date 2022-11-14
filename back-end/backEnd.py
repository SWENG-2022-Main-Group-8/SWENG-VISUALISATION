import json
import requests

username = input("Enter username: ")
url = "https://api.github.com/users/{}".format(username)

response = requests.get(url)
print(json.loads(response.text))