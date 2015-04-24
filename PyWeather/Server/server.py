import getxml
from forecastdata import ForecastDay

forecast_xml = getxml.xml_request('forecast', 'MO/Maryland_Heights')
print(forecast_xml)
somedate = ForecastDay(1429833600)
d = somedate.dateobj
print(d.day)