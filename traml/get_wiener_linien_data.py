"""
Get data from Weiner Linien data

Demo the use of a yaml function
"""
import json
import time
import yaml 
import requests
import obspy
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np

def wl_api_key(secrets_yaml="./traml/my_secrets.yaml"):
    """
    Returns the API key for wienerlinien account
    Expected to find in traml/my_secrets.yaml file
    """ 
    with open(secrets_yaml) as fh:
        doc = yaml.load(fh, Loader=yaml.Loader)
    api_key = doc["apis"]["wienerlinien"]["key"]
    return api_key

def read_monitors_of_line(rbl_request_id):
    """
    Get data from Weiner Linien on current transport table defined by the rbl_request_id
    Returns data
    """ 
    api_key = wl_api_key() 
    base_url = "http://www.wienerlinien.at/ogd_realtime/monitor"
    query = "?rbl={0}&activateTrafficInfo=stoerungkurz&activateTrafficInfo=stoerunglang&activateTrafficInfo=aufzugsinfo&sender={1}".format(rbl_request_id,api_key)
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'Accept' : 'application/json', 'Content-Type': 'application/json; charset=utf-8'}

    # sending get request and saving the response as response object
    res = requests.get(url = base_url + query, params = PARAMS)
    # extracting data in json format
    data = res.json()["data"]
    return data 
 
def wl_data(request_id):
    """
    Reformat the data provided by the request to WL.  
    """
    data = read_monitors_of_line(request_id)
    monitors = data['monitors'][0]
    station = monitors['locationStop']

    geometry = station['geometry']
    lines = monitors['lines'][0]
    depature = lines['departures']
    departure_time = depature['departure'][0]['departureTime']

    result = {}
    result['station'] = str(station['properties']['title'][0:8])
    result['coordinates'] = geometry['coordinates']
    result['line'] = str(lines['name'][0:8])
    result['towards'] = str(lines['towards'][0:8])
    result['timeplanned'] = obspy.UTCDateTime(departure_time['timePlanned'])
    result['timeReal'] = obspy.UTCDateTime(departure_time['timeReal'])
    return result

if __name__ == "__main__": 
    ### CHECK DEMO secrets yaml FILE EXISTS AND IS READABLE
    print(wl_api_key("./traml/my_sea_crates.yaml"))
    ## TRY REQUEST
    request_ids = [4627, 4439, 120, 99, 100, 119, 135, 136, 3516]
    result = wl_data(request_ids[0])
    print(result)
