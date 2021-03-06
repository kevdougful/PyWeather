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
try:
    # Python 3
    from urllib.request import urlopen
except ImportError:
    # Python 2
    from urllib2 import urlopen
from xml.dom.minidom import parseString

def _get_apikey():
    """Gets Wunderground API from api.key file.
    
    Returns:
        Wunderground API key from api.key file in same directory.
    """
    return open('./api.key').read()

def _get_url(requested_feature, request_query, response_format='xml', request_params=''):
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
        response_format: File format for request response (xml, gif, etc.).
        request_params: Additional parameters for radar API requests (optional).
            See: http://www.wunderground.com/weather/api/d/docs?d=layers/radar&MR=1

    Returns:
        HTTP URL for the desired location and type of request.
    """
    url = 'http://api.wunderground.com/api/'
    url += _get_apikey() + '/' + requested_feature + '/q/' + request_query + '.' + response_format + request_params
    return url

def xml_request(requested_feature, request_query):
    """Sends an HTTP request for XML for the desired location and request type

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
    # Get URL
    url = _get_url(requested_feature, request_query)
    # Send HTTP request
    http_request = urlopen(url)
    # Read response
    http_response = http_request.read()
    # Return parsed XML
    return parseString(http_response)

def radar_request(request_query, animated=True, response_format='gif', request_params=''):
    """Sends an HTTP request for a radar image from the API

    Args:
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
        animated: Whether to request an animated image.
        response_format: Image format to request (gif, png, swf).
        request_params: Additional parameters for radar API requests (optional).
            See: http://www.wunderground.com/weather/api/d/docs?d=layers/radar&MR=1

    Returns:
        A radar image.
    """
    # Get URL
    requested_feature = 'animatedradar' if animated else 'radar'
    url = _get_url(requested_feature, request_query, response_format, request_params)
    # Send HTTP request
    http_request = urlopen(url)
    # Read response
    http_response = http_request.read()
    # Return the image
    return http_response
