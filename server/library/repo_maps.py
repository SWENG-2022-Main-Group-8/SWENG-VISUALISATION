import requests
import json
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3


def getOrgData(organisation):
    countryDict = {}

#   Do until api fails
    for i in range(1):
        responseOrg = requests.get("https://api.github.com/orgs/{}/members?page40".format(organisation,i))
        orgData = responseOrg.json()
        
        print(orgData)
        for i in orgData:
            username = i["login"]
            # print(username)
            try:
                response = (requests.get("https://api.github.com/users/" + username))
            except requests.exceptions.RequestException as e:
                continue
            userData = response.json()
            location =userData["location"]
            if location != "None":
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

                
    print(countryDict)
    return json.dumps(countryDict, indent = 4)


        
getOrgData("facebook")


# geolocator = Nominatim(user_agent="Git Repo Mapper")
# location = geolocator.geocode("Trinity College Dublin, Dublin")
# print(location.address)
# googleGeolocator = GoogleV3(user_agent= "Git Repo Mapper")
# location = googleGeolocator.geocode("Trinity College Dublin")




