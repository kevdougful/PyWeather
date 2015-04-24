import getxml
from forecastdata import Forecast

forecast_xml = getxml.xml_request('forecast', 'MO/Maryland_Heights')
print(forecast_xml)
somedate = Forecast('MO/Maryland_Heights')