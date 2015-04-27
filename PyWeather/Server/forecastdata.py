from getxml import xml_request
from datetime import datetime

def _getNodeValue(element, tagname):
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
        epoch = _getNodeValue(simple, 'epoch')
        self.date = datetime.fromtimestamp(int(epoch))

        # txt_forecast elements
        self.day_icon = _getNodeValue(day, 'icon')
        self.nt_icon = _getNodeValue(night, 'icon')
        self.daytext = _getNodeValue(day, 'fcttext')
        self.nighttext = _getNodeValue(night, 'fcttext')
        self.daypop = int(_getNodeValue(day, 'pop')) # probability of precipitation
        self.nightpop = int(_getNodeValue(night, 'pop'))

        # simpleforecast elements
        self.period = int(_getNodeValue(simple, 'period'))
        
        high = simple.getElementsByTagName('high')
        self.high_F = int(_getNodeValue(high[0], 'fahrenheit'))
        
        low = simple.getElementsByTagName('low')
        self.low_F = int(_getNodeValue(low[0], 'fahrenheit'))
        
        self.humidity = _getNodeValue(simple, 'avehumidity')

        qpf_allday = simple.getElementsByTagName('qpf_allday') # quantity precip. fallen
        self.qpf_allday_in = float(_getNodeValue(qpf_allday[0], 'in'))

        qpf_day = simple.getElementsByTagName('qpf_day')
        self.qpf_day_in = float(_getNodeValue(qpf_day[0], 'in'))

        qpf_night = simple.getElementsByTagName('qpf_night')
        self.qpf_night_in = float(_getNodeValue(qpf_night[0], 'in'))

        maxwind = simple.getElementsByTagName('maxwind')
        self.maxwind_mph = int(_getNodeValue(maxwind[0], 'mph'))
        self.maxwind_degrees = float(_getNodeValue(maxwind[0], 'degrees'))
        print(self.maxwind_degrees)

        # metric values not implemented
        # snow_allday, snow_day, snow_night elements not implemented

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')