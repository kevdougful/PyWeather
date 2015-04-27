from getxml import xml_request
from datetime import datetime

def _getNodeValue(element, tagname):
    elemstr = element.toxml()
    # handle self closing tags
    if elemstr.find('/>', 0, len(elemstr)) > -1: 
        return 0.0
    else: 
        return element.getElementsByTagName(tagname)[0].firstChild.nodeValue

class Forecast(object):
    '''
    encapsulates a series of ForecastDay 
    objects
    '''
    def __init__(self, location):
        xml = xml_request('forecast', location)
        txt_forecast = xml.getElementsByTagName('txt_forecast')
        simpleforecast = xml.getElementsByTagName('simpleforecast')
        
        self.ForecastDays = list()

        # get all forecastday elements from simple forecast
        simplexml = list()
        for simpleday in simpleforecast[0].getElementsByTagName('forecastday'):
            simplexml.append(simpleday)

        txtdays = txt_forecast[0].getElementsByTagName('forecastday')

        # get day forecastday elements from text forecast
        dayxml = list()
        for i in range(0, 8, 2):
            dayxml.append(txtdays[i])

        # get night forecastday elements from text forecast
        nightxml = list()
        for i in range(1, 9, 2):
            nightxml.append(txtdays[i])

        #print(len(simplexml))
        #print(len(dayxml))
        #print(len(nightxml))

        # create ForecastDay objects
        for i in range(0, 4):
            self.ForecastDays.append(ForecastDay(dayxml[i], nightxml[i], simplexml[i]))

class ForecastDay(object):
    '''
    encapsulates all forecast data from a
    Wunderground API response
    '''
    def __init__(self, day, night, simple):
        # set the date
        epoch = simple.getElementsByTagName('epoch')[0].firstChild.nodeValue
        #epoch = _getNodeValue(simple, 'epoch')
        self.date = datetime.fromtimestamp(int(epoch))

        # txt_forecast elements
        self.day_icon = _getNodeValue(day, 'icon')
        self.nt_icon = _getNodeValue(night, 'icon')
        self.daytext = _getNodeValue(day, 'fcttext')
        self.nighttext = _getNodeValue(night, 'fcttext')
        self.daypop = int(_getNodeValue(day, 'pop')) # probability of precipitation
        self.nightpop = int(_getNodeValue(night, 'pop'))

        # simpleforecast elements
        self.period = simple.getElementsByTagName('period')[0].firstChild.nodeValue
        #self.period = int(_getNodeValue(simple, 'period'))
        
        high = simple.getElementsByTagName('high')
        self.high_F = int(_getNodeValue(high[0], 'fahrenheit'))
        
        low = simple.getElementsByTagName('low')
        self.low_F = int(_getNodeValue(low[0], 'fahrenheit'))
        
        self.humidity = simple.getElementsByTagName('avehumidity')[0].firstChild.nodeValue
        #self.humidity = _getNodeValue(simple, 'avehumidity')

        qpf_allday = simple.getElementsByTagName('qpf_allday') # quantity precip. fallen
        self.qpf_allday_in = float(_getNodeValue(qpf_allday[0], 'in'))

        qpf_day = simple.getElementsByTagName('qpf_day')
        self.qpf_day_in = float(_getNodeValue(qpf_day[0], 'in'))

        qpf_night = simple.getElementsByTagName('qpf_night')
        self.qpf_night_in = float(_getNodeValue(qpf_night[0], 'in'))

        maxwind = simple.getElementsByTagName('maxwind')
        self.maxwind_mph = int(_getNodeValue(maxwind[0], 'mph'))
        self.maxwind_degrees = float(_getNodeValue(maxwind[0], 'degrees'))
        self.maxwind_dir = _getNodeValue(maxwind[0], 'dir')

        # metric values not implemented
        # snow_allday, snow_day, snow_night elements not implemented

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')

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