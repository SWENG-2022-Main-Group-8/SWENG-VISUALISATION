import json
import requests

def organizationList(ORG):
    try:
        url = "https://api.github.com/org/" + ORG + "/members"
        response = requests.get(url)
        return json.loads(response.text)
    except:
        print("organization could not be found")
        return '{}'