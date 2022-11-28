import requests
import json
from itertools import takewhile

none = "None"

def getOrgLocationData(organisation):
    countryDict = {}
    #   Do until api fails
    
    url = ("https://api.github.com/orgs/{}/members?page=1".format(organisation))
    res=requests.get(url)
    orgData=res.json()


    while 'next' in res.links.keys():
        res=requests.get(res.links['next']['url'])
        orgData.extend(res.json())
        
    print(orgData)
    for i in orgData:
        username = i["login"]
        # print(username)
        try:
            response = requests.get("https://api.github.com/users/" + username)
        except requests.exceptions.RequestException as e:
            continue
        userData = response.json()
        location =userData["location"]
        if location is not None:
            response = requests.get("https://nominatim.openstreetmap.org/search?q={}&format=json&addressdetails=1&limit=1".format(location))
            responseJsonFile = response.json()
            print("")
            print(location)
            print("country code : "+responseJsonFile[0]['address']['country_code'])
            countryCode = responseJsonFile[0]['address']['country_code']

            try:                    
                countryDict[countryCode] = countryDict[countryCode]+1
            except KeyError:
                countryDict[countryCode] = 1
        else:
            countryCode = "int"

            try:                    
                countryDict[countryCode] = countryDict[countryCode]+1
            except KeyError:
                countryDict[countryCode] = 1

    print(countryDict)
    return countryDict
    
# For testing purposes only!
# getOrgLocationData("FT-Autonomous")





