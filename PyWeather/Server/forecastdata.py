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
"""
from getxml import xml_request
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
    def __init__(self, location):
        xml = xml_request('forecast', location)
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
        minwind_degrees: Forecasted prevailing wind direction (compass heading 0-360°).
        minwind_dir: Forecasted prevailing wind direction (e.g. NNE).
        maxwind_mph: Maximum wind speed forecasted (miles per hour).
        maxwind_degrees: Forecasted prevailing wind direction (compass heading 0-360°).
        maxwind_dir: Forecasted prevailing wind direction (e.g. NNE).
    """
    def __init__(self, day, night, simple):
        # set the date
        epoch = simple.getElementsByTagName('epoch')[0].firstChild.nodeValue
        self.forecast_date = datetime.fromtimestamp(int(epoch))

        # txt_forecast elements
        self.day_icon = _getNodeValue(day, 'icon')
        self.night_icon = _getNodeValue(night, 'icon')
        self.day_text = _getNodeValue(day, 'fcttext')
        self.night_text = _getNodeValue(night, 'fcttext')
        
        # probability of precipitation
        self.pop = simple.getElementsByTagName('pop')[0].firstChild.nodeValue
        self.day_pop = int(_getNodeValue(day, 'pop'))
        self.night_pop = int(_getNodeValue(night, 'pop'))

        # simpleforecast elements
        self.period = simple.getElementsByTagName('period')[0].firstChild.nodeValue
        
        high = simple.getElementsByTagName('high')
        self.high_F = int(_getNodeValue(high[0], 'fahrenheit'))
        
        low = simple.getElementsByTagName('low')
        self.low_F = int(_getNodeValue(low[0], 'fahrenheit'))
        
        self.humidity = simple.getElementsByTagName('avehumidity')[0].firstChild.nodeValue

        # quantity precipitation forecasted
        qpf_allday = simple.getElementsByTagName('qpf_allday')
        self.qpf_allday_in = float(_getNodeValue(qpf_allday[0], 'in'))

        qpf_day = simple.getElementsByTagName('qpf_day')
        self.qpf_day_in = float(_getNodeValue(qpf_day[0], 'in'))

        qpf_night = simple.getElementsByTagName('qpf_night')
        self.qpf_night_in = float(_getNodeValue(qpf_night[0], 'in'))
        
        # wind
        minwind = simple.getElementsByTagName('avewind')
        self.minwind_mph = int(_getNodeValue(minwind[0], 'mph'))
        self.minwind_degrees = float(_getNodeValue(minwind[0], 'degrees'))
        self.minwind_dir = _getNodeValue(minwind[0], 'dir')
        maxwind = simple.getElementsByTagName('maxwind')
        self.maxwind_mph = int(_getNodeValue(maxwind[0], 'mph'))
        self.maxwind_degrees = float(_getNodeValue(maxwind[0], 'degrees'))
        self.maxwind_dir = _getNodeValue(maxwind[0], 'dir')
        
        # metric values not implemented
        # snow_allday, snow_day, snow_night elements not implemented

    def __str__(self):
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

    #@staticmethod
    #def degreesToDirection(deg):
    #    '''
    #    convert 0-360° float to three letter heading (e.g. NNE)
    #    '''
    #    if deg < 0 or deg > 360:
    #        raise Exception('degree value must be 0-360')
    #    elif deg >= 0 and deg <= 11.25: return 'N'
    #    elif deg > 348.75 and deg <= 360: return "N"
    #    elif deg > 11.25 and deg <= 33.75: return "NNE"
    #    elif deg > 33.75 and deg <= 56.25: return "NE"
    #    elif deg > 56.25 and deg <= 78.75: return "ENE"
    #    elif deg > 78.75 and deg <= 101.25: return "E"
    #    elif deg > 101.25 and deg <= 123.75: return "ESE"
    #    elif deg > 123.75 and deg <= 146.25: return "SE"
    #    elif deg > 146.25 and deg <= 168.75: return "SSE"
    #    elif deg > 168.75 and deg <= 191.25: return "S"
    #    elif deg > 191.25 and deg <= 213.75: return "SSW"
    #    elif deg > 213.75 and deg <= 236.25: return "SW"
    #    elif deg > 236.25 and deg <= 258.75: return "WSW"
    #    elif deg > 258.75 and deg <= 281.25: return "W"
    #    elif deg > 281.25 and deg <= 303.75: return "WNW"
    #    elif deg > 303.75 and deg <= 326.25: return "NW"
    #    elif deg > 326.25 and deg <= 348.75: return "NNW"