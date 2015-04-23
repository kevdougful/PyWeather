from urllib import request
import json

# get the api key
def _get_apikey():
    return open('./api.key').read()

# construct a request URL
def _get_url(type, location):
    # build up URL
    url = 'http://api.wunderground.com/api/'
    url += _get_apikey() + '/' + type + '/q/' + location + '.json'
    return url

def api_request(type, location):
    # get URL
    url = _get_url(type, location)
    # send http request
    forecast_req = request.urlopen(url)
    # read response
    forecast_res = forecast_req.read().decode()
    # return parsed json
    return json.loads(forecast_res)