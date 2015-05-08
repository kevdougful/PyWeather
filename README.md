# PyCaster
___
This project provides Python utilities for creating and sending Wunderground API HTTP requests, parsing the reponse and manipulating SVG files for display.

## [getxml.py](PyWeather/Server/getxml.py)
This module handles forming an HTTP request, sending it to the Wundergroup API and returning the response as parsed XML.

### \_get\_apikey()
This method gets a Wunderground API key from an api.key file located in the same directory as the calling script.

### \_get_url(type, location)
Returns an HTTP URL for the desired location and type of API request
- __location__ - Acceptable values:
  - State/city combination: e.g. MO/St_Louis
  - ZIP Code: e.g. 63167
- __type__ - Acceptable values:
  - __forecast__
  - currently no other API requests are supported

### xml_request(type, location)
Makes an HTTP request for the desired location and type of API request and returns the response as parsed XML.
- __location__ - Acceptable values:
  - State/city combination: e.g. MO/St_Louis
  - ZIP Code: e.g. 63167
- __type__ - Acceptable values:
  - __forecast__
  - currently no other API requests are supported
  
## [forecastdata.py](PyWeather/Server/forecastdata.py)
This module contains class implementations of API responses.
### Forecast
This class is responsible for forming and sending the HTTP request.  It then does a higher-order parse on the XML response, creating a list of ForecastDay objects.  
The \_\_init\_\_() method for the Forecast class takes one argument for the location for which the forecast should be requested.  This argument is a string in the form:
    
`<State>/<City>` or `<Zip Code>`

### ForecastDay
This class encapsulates all forecast data returned by the API for a particular day.
#### ForecastDay Attributes:
* __forecast_date__: datetime object for day the ForecastDay object represents
* __day_icon__: icon name (according to Wunderground API presets) for that day's forecasted conditions
* __night_icon__: icon name (according to Wunderground API presets) for that night's forecasted conditions
* __day_text__: short description for that day's forecast
* __night_text__: short description for that night's forecast
* __pop__: propbability of precipitation for that entire day
* __day_pop__: propbability of precipitation for that day
* __night_pop__: propbability of precipitation for that night
* __period__: the relative chronological position of the ForecastDay within the forecast (1 is today)
* __high_F__: forecasted high temperature in fahrenheit
* __low_F__: forecasted low temperature in fahrenheit
* __qpf\_allday\_in__: quantity of precipitation in inches forecasted for the entire day
* __qpf\_day\_in__: quantity of precipitation in inches forecasted for the day
* __qpf\_night\_in__: quantity of precipitation in inches forecasted for the night
* __minwind\_mph__: minimum wind speed in MPH forecasted for day
* __minwind\_degrees__: forecasted wind direction in degrees
* __minwind\_dir__: forecasted wind direction by cardinal direction (e.g. NNE or SE)
* __maxwind\_mph__: maximum wind speed in MPH forecasted for day
* __maxwind\_degrees__: forecasted wind direction in degrees
* __maxwind\_dir__: forecasted wind direction by cardinal direction (e.g. NNE or SE)

_At this time, metric values are not implemented.  However, Wunderground API does provide these values and will eventually be available_  
_Snow will be supported at some point also._  

#### \_\_str\_\_() implementation:
The \_\_str\_\_() method of ForecastDay returns a nicely formatted string containing most of the data listed above.  

Below is an example of this output:  
```
Friday May-01-2015
    High: 73
    Low: 52
    Humidity: 45
    precip: 0.0"
    chance: 0%
    winds: NNW @ 6-10mph
    Day-time:
            Sunny skies. High 73F. Winds NNW at 5 to 10 mph.
            precip: 0.0"
            chance: 0%
    Night-time:
            Partly cloudy. Low 52F. Winds light and variable.
            precip: 0.0"
            chance: 10%
```
## [svgmanip.py](PyWeather/Server/svgmanip.py)
This module provides methods for populating an SVG template with Wunderground API forecast data.

### write\_forecast(forecast_obj)
Populates template.svg with a Forecast object data
- __forecast_obj__: Forecast object

### write\_forecastday(svg, forecastday_obj)
Writes ForecastDay object data to a given block of SVG
- __svg__: SVG block
- __forecastday_obj__: ForecastDay object

### _parse\_text(text)
Parses forecast text by removing Low/High and Wind info and splits into a 2-element array depending on length.  
- __text__: forecast text to parse

_this string_
```
  "A few clouds. A stray shower or thunderstorm is possible. Low 63F. Winds SSE at 10 to 15 mph."
```
_becomes_  
```
  [0] => "A few clouds. A stray shower"  
  [1] => "or thunderstorm is possible."  
```

### _wrap_text(text)
Splits a long line of text into two lines (if needed)
- __text__: forecast text to wrap.

## [convert.py](PyWeather/Server/convert.py)
This module provides functions for various unit conversions.  The module is structured into classes such that the user may import only the type of coversion functions desired.
    
``` python
from convert import temperature

freezing_point_F = temperature.c_to_f(0)
```

### temperature
Temperature conversion functions
#### f_to_c(fahrenheit)
Converts fahrenheit to celcius
- __fahrenheit__: fahrenheit value to convert

#### c_to_f(celcius)
Converts celcius to fahrenheit
- __celcius__: celcius value to convert