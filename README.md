# PyCaster
___
This project provides Python utilities for creating and sending Wunderground API HTTP requests, parsing the reponse and manipulating SVG files for display.

## forecastdata.py
This module contains class implementations of API responses.
### Forecast
This class is responsible for forming and sending the HTTP request.  It then does a higher-order parse on the XML response, creating a list of ForecastDay objects.  
The \_\_init\_\_() method for the Forecast class takes one argument for the location for which the forecast should be requested.  This argument is a string in the form:
    
`<State>/<City>` or `<Zip Code>`

### ForecastDay
This class encapsulates all forecast data returned by the API for a particular day.
#### ForecastDay Attributes:
* __date__: datetime object for day the ForecastDay object represents
* __day_icon__: icon name (according to Wunderground API presets) for that day's forecasted conditions
* __night_icon__: icon name (according to Wunderground API presets) for that night's forecasted conditions
* __daytext__: short description for that day's forecast
* __nighttext__: short description for that night's forecast
* __pop__: propbability of precipitation for that entire day
* __daypop__: propbability of precipitation for that day
* __nightpop__: propbability of precipitation for that night
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