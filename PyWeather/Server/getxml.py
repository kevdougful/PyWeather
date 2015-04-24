'''
getxml.py

This module handles forming an HTTP request and sending it to
the Wunderground API.  The parsed XML response is returned.
'''

from urllib import request
from xml.dom.minidom import parseString

# get the api key
def _get_apikey():
    return open('./api.key').read()

# construct a request URL
def _get_url(type, location):
    # build up URL
    url = 'http://api.wunderground.com/api/'
    url += _get_apikey() + '/' + type + '/q/' + location + '.xml'
    return url

# send API HTTP request
def xml_request(type, location):
    # get URL
    url = _get_url(type, location)
    # send HTTP request
    req = request.urlopen(url)
    # read response
    res = req.read()
    # return parsed XML
    return parseString(res)