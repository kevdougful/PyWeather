"""Handles forming an HTTP request and sending it to the Wunderground API.  

This file is part of PyWeather.

PyWeather is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyWeather is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyWeather.  If not, see <http://www.gnu.org/licenses/>.
"""

from urllib import request
from xml.dom.minidom import parseString

def _get_apikey():
    """Gets Wunderground API from api.key file.
    
    Returns:
        Wunderground API key from api.key file in same directory.
    """
    return open('./api.key').read()

def _get_url(request_type, requested_location):
    """Forms an URL using an API key, the type of request, and location desired.

    Args:
        request_type: Type of API request to send (forecast, 10 day forecast).
        requested_location: Geographical location for which to request.
            Acceptable forms:
                <State>/<City> (e.g. MO/St_Louis)
                <ZIP Code> (e.g. 63167)

    Returns:
        HTTP URL for the desired location and type of request.
    """
    url = 'http://api.wunderground.com/api/'
    url += _get_apikey() + '/' + request_type + '/q/' + requested_location + '.xml'
    return url

def xml_request(request_type, requested_location):
    """Sends an HTTP request for the desired location and request type

    Args:
        request_type: Type of API request to send (forecast, 10 day forecast).
        requested_location: Geographical location for which to request.
            Acceptable forms:
                <State>/<City> (e.g. MO/St_Louis)
                <ZIP Code> (e.g. 63167)

    Returns:
        HTTP response as parsed XML.
    """
    # get URL
    url = _get_url(request_type, requested_location)
    # send HTTP request
    req = request.urlopen(url)
    # read response
    res = req.read()
    # return parsed XML
    return parseString(res)