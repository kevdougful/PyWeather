from getxml import xml_request
from datetime import datetime

class Forecast(object):
    '''
    encapsulates a series of ForecastDay 
    objects
    '''
    def __init__(self, location):
        xml = xml_request('forecast', location)
        txt_forecast = xml.getElementsByTagName('txt_forecast')
        simpleforecast = xml.getElementsByTagName('simpleforecast')
        
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
            ForecastDay(dayxml[i], nightxml[i], simplexml[i])

class ForecastDay(object):
    '''
    encapsulates all forecast data from a
    Wunderground API response
    '''
    def __init__(self, day, night, simple):
        epoch = simple.getElementsByTagName('epoch')[0].firstChild.nodeValue
        self.date = datetime.fromtimestamp(int(epoch))
        self.day_icon = day.getElementsByTagName('icon')[0].firstChild.nodeValue
        self.nt_icon = night.getElementsByTagName('icon')[0].firstChild.nodeValue
        print(self.nt_icon)