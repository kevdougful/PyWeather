class ForecastDay(object):
    '''
    Encapsulates all forecast data from a
    Wunderground API response
    '''

    def __init__(self, date):
        self.date = date
