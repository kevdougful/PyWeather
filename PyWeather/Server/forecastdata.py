from getxml import xml_request
from datetime import datetime

# get element(s) from XML
def _getelements(xml, element):
    'returns a specific element from some XML'
    return xml.getElementsByTagName(element)

class Forecast(object):
    '''
    encapsulates a series of ForecastDay 
    objects
    '''
    def __init__(self, location):
        self.xml = xml_request('forecast', location)
        self.txt_forecast = _getelements(self.xml, 'txt_forecast')
        self.simpleforecast = _getelements(self.xml, 'simpleforecast')
        #days = self.txt_forecast[0].childNodes[1].getElementsByTagName('forecastday')
        #print(len(days))
        days = self.xml.getElementsByTagName('forecastday')
        print(days[0].toprettyxml())
        #print(len(days))
        #for item in self.txt_forecast[0].childNodes:
        #    if item.nodeType == 1:
        #        days = item.getElementsByTagName('forecastday')
        #        print(len(days))

class ForecastDay(object):
    '''
    encapsulates all forecast data from a
    Wunderground API response
    '''
    def __init__(self, xml):
        self.xml = xml