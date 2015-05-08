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

Inspiration as well as coding strategies are borrowed heavily from
Matthew Petroff's Kindle Weather Display project.

http://mpetroff.net/2012/09/kindle-weather-display/
https://github.com/mpetroff/kindle-weather-display
"""

from urllib import request
from xml.dom.minidom import parseString

def _get_apikey():
    """Gets Wunderground API from api.key file.
    
    Returns:
        Wunderground API key from api.key file in same directory.
    """
    return open('./api.key').read()

def _get_url(requested_feature, request_query):
    """Forms an URL using an API key, the type of request, and location desired.

    Args:
        requested_feature: Type of API request to send (forecast, 10 day forecast).
        request_query: Geographical location for which to request.
            Acceptable forms:
                <State>/<City> (e.g. MO/St_Louis)
                <ZIP Code> (e.g. 63167)
                <County>/<City? (e.g. Australia/Sydney)
                <latitude>/<longitude> (e.g. 37.8,-122.4)
                <Airport code> (e.g. KJFK)
                <PWS id> (e.g. pws:KCASANFR70)
                AutoIP (e.g. autoip)
                specific IP (e.g. autoip.xml?geo_ip=38.102.136.138)

    Returns:
        HTTP URL for the desired location and type of request.
    """
    url = 'http://api.wunderground.com/api/'
    url += _get_apikey() + '/' + requested_feature + '/q/' + request_query + '.xml'
    return url

def xml_request(requested_feature, request_query):
    """Sends an HTTP request for the desired location and request type

    Args:
        requested_feature: Type of API request to send (forecast, 10 day forecast).
        request_query: Geographical location for which to request.
            Acceptable forms:
                <State>/<City> (e.g. MO/St_Louis)
                <ZIP Code> (e.g. 63167)
                <County>/<City? (e.g. Australia/Sydney)
                <latitude>/<longitude> (e.g. 37.8,-122.4)
                <Airport code> (e.g. KJFK)
                <PWS id> (e.g. pws:KCASANFR70)
                AutoIP (e.g. autoip)
                specific IP (e.g. autoip.xml?geo_ip=38.102.136.138)

    Returns:
        HTTP response as parsed XML.
    """
    # get URL
    url = _get_url(requested_feature, request_query)
    # send HTTP request
    req = request.urlopen(url)
    # read response
    res = req.read()
    # return parsed XML
    return parseString(res)