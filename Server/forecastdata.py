"""Classes for encapsulating forecast data.

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
from apirequest import xml_request
from datetime import datetime

def _getNodeValue(xml_element, tag_name):
    """Extracts the enclosed text from a specific tag within an XML element

    Args:
        xml_element: XML element to extract from.
        tag_name: Specific tag (by name) from which to extract enclosed text.

    Returns:
        The enclosed text.

    """
    element_string = xml_element.toxml()
    # handle self closing tags
    if element_string.find('/>', 0, len(element_string)) > -1: 
        return 0.0
    else: 
        return xml_element.getElementsByTagName(tag_name)[0].firstChild.nodeValue

class Forecast(object):
    """Encapsulates all data from a particular forecast.

    This class is responsible for making the API request and parsing and storing
    the response data in a collection of ForecastDay objects.

    Attributes:
        ForecastDays: list of ForecastDay objects containing the forecast's data.
    """
    def __init__(self, request_query):
        """Creates a new instance of the Forecast class.

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

        Returns:
            A new instance of the Forecast class.
        """
        xml = xml_request('forecast', request_query)
        txt_forecast = xml.getElementsByTagName('txt_forecast')
        simpleforecast = xml.getElementsByTagName('simpleforecast')
        
        self.ForecastDays = list()

        # The API response is broken into two main sections: txt_forecast and
        # simpleforecast.  txt_forecast contains data for day and night,
        # including a short, plain english description of the data.
        # simpleforecast contains data for each calendar day but does not
        # include any descriptions.  The Forecast object is responsible to 
        # creating ForecastDay objects that contain all the data from both
        # txt_forecast and simpleforecast for a particular calendar day.

        # Get all forecastday elements from simple forecast
        simplexml = list()
        for simpleday in simpleforecast[0].getElementsByTagName('forecastday'):
            simplexml.append(simpleday)

        # Get all periods in the txt_forecast
        txtdays = txt_forecast[0].getElementsByTagName('forecastday')

        # Get day forecastday elements from txt_forecast
        dayxml = list()
        for i in range(0, 8, 2):
            dayxml.append(txtdays[i])

        # Get night forecastday elements from txt_forecast
        nightxml = list()
        for i in range(1, 9, 2):
            nightxml.append(txtdays[i])

        # Create ForecastDay objects
        for i in range(0, 4):
            self.ForecastDays.append(ForecastDay(dayxml[i], nightxml[i], simplexml[i]))

class ForecastDay(object):
    """Encapsulates data from both txt_forecast and simpleforecast for a single day.
    
    txt_forecast contains data for day and night, including a short, plain 
    english description of the data. simpleforecast contains data for each
    calendar day but does not include any descriptions.

    Attributes:
        forecast_date: datetime object for day this object represents.
        day_icon: SVG icon name to use for the day-time forecast.
        night_icon: SVG icon name to use for the night-time forecast.
        day_text: Plain english description of the day-time forecast.
        night_text: Plain english description of the night-time forecast.
        pop: Probability of precipitation for entire day.
        day_pop: Probability of precipitation for day-time.
        night_pop: Probability of precipitation for night-time.
        period: Relative position of day in the rest of the forecast (1 = today).
        high_F: Forecasted high temperature (fahrenheit).
        low_F: Forecasted low temperature (fahrenheit).
        humidity: Forecasted relative humidity.
        qpf_allday_in: Quantity of precipitation forecasted for entire day (inches).
        qpf_day_in: Quantity of precipitation forecasted for day-time (inches).
        qpf_night_in: Quantity of precipitation forecasted for night-time (inches).
        minwind_mph: Minimum wind speed forecasted (miles per hour).
        minwind_degrees: Forecasted prevailing wind direction (compass heading 0-360).
        minwind_dir: Forecasted prevailing wind direction (e.g. NNE).
        maxwind_mph: Maximum wind speed forecasted (miles per hour).
        maxwind_degrees: Forecasted prevailing wind direction (compass heading 0-360).
        maxwind_dir: Forecasted prevailing wind direction (e.g. NNE).
    """
    def __init__(self, day_xml, night_xml, simple_xml):
        """Creates a new instance of the ForecastDay class.

        Args:
            day_xml: The day-time periods of the txt_forecast section.
            night_xml: The day-time periods of the txt_forecast section.
            simple_xml: The simpleforecast section of the API response.

        Returns:
            A new instance of the ForecastDay class.
        """
        # NOTE:
        # metric values not yet implemented
        # snow_allday, snow_day, snow_night elements not yet implemented

        # set the date
        epoch = simple_xml.getElementsByTagName('epoch')[0].firstChild.nodeValue
        self.forecast_date = datetime.fromtimestamp(int(epoch))

        # txt_forecast elements
        self.day_icon = _getNodeValue(day_xml, 'icon')
        self.night_icon = _getNodeValue(night_xml, 'icon')
        self.day_text = _getNodeValue(day_xml, 'fcttext')
        self.night_text = _getNodeValue(night_xml, 'fcttext')
        
        # probability of precipitation
        self.pop = simple_xml.getElementsByTagName('pop')[0].firstChild.nodeValue
        self.day_pop = int(_getNodeValue(day_xml, 'pop'))
        self.night_pop = int(_getNodeValue(night_xml, 'pop'))

        # simpleforecast elements
        self.period = simple_xml.getElementsByTagName('period')[0].firstChild.nodeValue
        
        high = simple_xml.getElementsByTagName('high')
        self.high_F = int(_getNodeValue(high[0], 'fahrenheit'))
        
        low = simple_xml.getElementsByTagName('low')
        self.low_F = int(_getNodeValue(low[0], 'fahrenheit'))
        
        self.humidity = simple_xml.getElementsByTagName('avehumidity')[0].firstChild.nodeValue

        # quantity precipitation forecasted
        qpf_allday = simple_xml.getElementsByTagName('qpf_allday')
        self.qpf_allday_in = float(_getNodeValue(qpf_allday[0], 'in'))

        qpf_day = simple_xml.getElementsByTagName('qpf_day')
        self.qpf_day_in = float(_getNodeValue(qpf_day[0], 'in'))

        qpf_night = simple_xml.getElementsByTagName('qpf_night')
        self.qpf_night_in = float(_getNodeValue(qpf_night[0], 'in'))
        
        # wind
        minwind = simple_xml.getElementsByTagName('avewind')
        self.minwind_mph = int(_getNodeValue(minwind[0], 'mph'))
        self.minwind_degrees = float(_getNodeValue(minwind[0], 'degrees'))
        self.minwind_dir = _getNodeValue(minwind[0], 'dir')
        maxwind = simple_xml.getElementsByTagName('maxwind')
        self.maxwind_mph = int(_getNodeValue(maxwind[0], 'mph'))
        self.maxwind_degrees = float(_getNodeValue(maxwind[0], 'degrees'))
        self.maxwind_dir = _getNodeValue(maxwind[0], 'dir')
        
    def __str__(self):
        """Creates a neatly formatted string using this object's encapsulated data.

        Returns:
            Neatly formatted string using this object's encapsulated data.
        """
        output = self.forecast_date.strftime('%A %b-%d-%Y') + '\n'
        output += '\tHigh: ' + str(self.high_F) + '\n'
        output += '\tLow: ' + str(self.low_F) + '\n'
        output += '\tHumidity: ' + str(self.humidity) + '\n'
        output += '\tprecip: ' + str(self.qpf_allday_in) + '\"\n'
        output += '\tchance: ' + str(self.pop) + '%\n'
        output += '\twinds: ' + self.minwind_dir + ' @ ' \
            + str(self.minwind_mph) + '-' + str(self.maxwind_mph) + 'mph\n'
        output += '\tDay-time:\n'
        output += '\t\t' + self.day_text + '\n'
        output += '\t\tprecip: ' + str(self.qpf_day_in) + '\"\n'
        output += '\t\tchance: ' + str(self.day_pop) + '%\n'
        output += '\tNight-time:\n'
        output += '\t\t' + self.night_text + '\n'
        output += '\t\tprecip: ' + str(self.qpf_night_in) + '\"\n'
        output += '\t\tchance: ' + str(self.night_pop) + '%\n'
        return output