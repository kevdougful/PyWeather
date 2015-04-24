import getxml

forecast_xml = getxml.xml_request('forecast', 'MO/Maryland_Heights')
print(forecast_xml)