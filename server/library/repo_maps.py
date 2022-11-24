import requests
import json
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
# responseOrg = requests.get("https://api.github.com/orgs/facebook/public_members")
# orgData = responseOrg.json()
# # print(orgData)
# for i in orgData:
#     username = i["login"]
#     # print(username)
#     try:
#         response = (requests.get("https://api.github.com/users/" + username))
#     except requests.exceptions.RequestException as e:
#         continue
#     userData = response.json()
#     location =userData["location"]
#     print(location)




geolocator = Nominatim(user_agent="Git Repo Mapper")
location = geolocator.geocode("Trinity College Dublin, Dublin")
print(location.raw)
# googleGeolocator = GoogleV3(user_agent= "Git Repo Mapper")
# location = googleGeolocator.geocode("Trinity College Dublin")




