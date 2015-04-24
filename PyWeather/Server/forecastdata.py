from datetime import datetime

class ForecastDay(object):
    '''
    Encapsulates all forecast data from a
    Wunderground API response
    '''
    def __init__(self, epoch):
        self.epoch = epoch
        self.dateobj = datetime.fromtimestamp(epoch)