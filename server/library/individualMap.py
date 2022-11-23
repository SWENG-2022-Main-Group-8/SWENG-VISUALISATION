from geopy.geocoders import Nominatim
import json 

def getLatLng(address):
    try:
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(address)
        coordinates = {'latitude':location.latitude, 'longitude':location.longitude}
        return coordinates
    except:
        print("Invalid Address")
        return 

def mergeDictionary(dict1, dict2):
    if(dict1!= None and dict2!= None):
        result = dict1 | dict2
        return result
    else:
        return dict1