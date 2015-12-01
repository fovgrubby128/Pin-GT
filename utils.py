'''
Helpers functions used by main view controller
'''

import urllib2, json
import googlemaps
from crawler import crawler

API_KEY = 'AIzaSyDtaF7VqFqOIQaS0N-gSiWRPfOTI8UXN7Q'

def getEventsByDay(start_date, end_date, tag):
    results = crawler(start_date, end_date)
    if tag == 'All':
        return results
    entries = [e for e in results if tag in e['Tag']]
    return entries

'''
given an array of location, make request to Google API and translate
them into longitude and latitude
'''
def processGeoInfo(entries):
    baseURL = "https://maps.googleapis.com/maps/api/geocode/json?address="
    l = []
    for entry in entries:
        loc = entry['Location']
        url = baseURL + "Georgia%20Tech,%20" + loc
        url = url.replace(" ", "%20")
        raw = urllib2.urlopen(url)
        raw = raw.read()
        resp = json.loads(raw)
        if len(resp["results"]) > 0:
            entry['latlon'] = resp["results"][0]["geometry"]["location"]
            ndigit = 7
            entry['latlon']['lat'] = round(entry['latlon']['lat'], ndigit)
            entry['latlon']['lng'] = round(entry['latlon']['lng'], ndigit)
            l.append(entry)
    return l

'''
given an location name, return a tuple of (lat, lng)
'''
def locationToGeo(loc):
    gmaps = googlemaps.Client(key=API_KEY)
    geocode_result = gmaps.geocode(loc)
    lonlat = geocode_result[0]['geometry']['location']
    return (lonlat['lat'], lonlat['lng'])