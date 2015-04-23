import getjson

cast_json = getjson.api_request('forecast', 'MO/Maryland_Heights')
print(cast_json)