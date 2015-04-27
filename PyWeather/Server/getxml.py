'''
getxml.py

This module handles forming an HTTP request and sending it to
the Wunderground API.  The parsed XML response is returned.
'''

from urllib import request
from xml.dom.minidom import parseString

def _get_apikey():
    '''
    gets Wunderground API from api.key file.
    api.key file must be in same directory.
    '''
    return open('./api.key').read()

def _get_url(type, location):
    '''
    returns an HTTP URL for the desired location and type of request.
    '''
    url = 'http://api.wunderground.com/api/'
    url += _get_apikey() + '/' + type + '/q/' + location + '.xml'
    return url

def xml_request(type, location):
    '''
    makes an HTTP request for desired location and type of request.
    returns the response as parsed XML.
    '''
    # get URL
    url = _get_url(type, location)
    # send HTTP request
    req = request.urlopen(url)
    # read response
    res = req.read()
    # return parsed XML
    return parseString(res)