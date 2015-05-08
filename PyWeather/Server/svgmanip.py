"""Provides tools for populating and SVG template with Forecast object data.

This file is part of PyWeather.

PyWeather is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyWeather is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyWeather.  If not, see <http://www.gnu.org/licenses/>.

Inspiration as well as coding strategies are borrowed heavily from
Matthew Petroff's Kindle Weather Display project.

http://mpetroff.net/2012/09/kindle-weather-display/
https://github.com/mpetroff/kindle-weather-display
"""
import codecs

def write_forecast(forecast_obj):
    """Opens an SVG file and populates it with Forecast data.

    Args:
        forecast_obj: Forecast object containing data to populate.

    Returns:
        None.
    """
    # Open the SVG template (read-only)
    output = codecs.open('./template.svg', 'r', encoding='utf-8').read()
    for day in forecast_obj.ForecastDays:
        # Write each day to the opened SVG file
        output = write_forecastday(output, day)
    # Save the populated SVG file
    codecs.open('forecast.svg', 'w', encoding='utf-8').write(output)

def write_forecastday(svg, forecastday_obj):
    """Populates an opened SVG file with data from a ForecastDay object.

    Args:
        svg: An opened SVG file.
        forecastday_obj: ForecastDay object containing data to populate.

    Returns:
        The opened SVG file with newly populated data.
    """
    # Get the ForecastDay's position (period) in the Forecast
    period = forecastday_obj.period

    # Icons
    svg = svg.replace('P' + period + 'I1', forecastday_obj.day_icon)
    svg = svg.replace('P' + period + 'I2', forecastday_obj.night_icon)

    period = 'period' + period

    # Text
    svg = svg.replace(period + 'title', forecastday_obj.forecast_date.strftime('%a %b-%d'))
    daytext = _clean_text(forecastday_obj.day_text)
    nighttext = _clean_text(forecastday_obj.night_text, 40)
    svg = svg.replace(period + 'daytext1', daytext[0])
    svg = svg.replace(period + 'daytext2', daytext[1])
    svg = svg.replace(period + 'nighttext1', nighttext[0])
    svg = svg.replace(period + 'nighttext2', nighttext[1])

    # High, low, humidity
    svg = svg.replace(period + 'high', str(forecastday_obj.high_F) + 'F')
    svg = svg.replace(period + 'low', str(forecastday_obj.low_F) + 'F')
    svg = svg.replace(period + 'humidity', str(forecastday_obj.humidity) + '%')

    # Rain info
    svg = svg.replace(period + 'dayrainchance', str(forecastday_obj.day_pop) + '%')
    svg = svg.replace(period + 'nightrainchance', str(forecastday_obj.night_pop) + '%')
    svg = svg.replace(period + 'dayrainamount', str(forecastday_obj.qpf_day_in) + '\"')
    svg = svg.replace(period + 'nightrainamount', str(forecastday_obj.qpf_night_in) + '\"')
    return svg

def _clean_text(forecast_text, break_length=65):
    """Cleans forecast text for display in SVG template

    The API response contains plain english desciptions of the day's 
    forecast.  These strings always contain a summary of the high,
    low, and wind speed/direction.  This information is captured in
    other attributes of the ForecastDay class.  Also, the forecast
    text is often too long to display on one line in the SVG
    template, so this method splits long lines into an array of two
    lines.

    Args:
        forecast_text: Long, verbose string of forecast text to clean.
        break_length: Position to look for whitespace to break the line.

    Returns:
        A 2-element array containing cleaned forecast text.
    """
    new_end = forecast_text.find('High')
    if new_end == -1:
        new_end = forecast_text.find('Low')
    if new_end > -1:
        forecast_text = forecast_text[:new_end - 1]
    return _wrap_text(forecast_text, break_length)

def _wrap_text(forecast_text, break_length):
    """Splits a long line of text into two lines

    Args:
        forecast_text: Long string of forecast text to split into 2 lines.
        break_length: Position to look for whitespace to break the line.
    Returns:
        A 2-element array containing forecast text.
    """
    wrapped_text = ['', '']
    if len(forecast_text) <= break_length:
        # Don't wrap short strings
        wrapped_text[0] = forecast_text
    else:
        br = forecast_text.find(' ', break_length)
        wrapped_text[0] = forecast_text[:br]
        wrapped_text[1] = forecast_text[br:]
    return wrapped_text