import requests
import json

responseOrg = requests.get("https://api.github.com/orgs/facebook/public_members")
orgData = responseOrg.json()
# print(orgData)
for i in orgData:
    username = i["login"]
    # print(username)
    try:
        response = (requests.get("https://api.github.com/users/" + username))
    except requests.exceptions.RequestException as e:
        continue
    userData = response.json()
    location =userData["location"]
    print(location)

