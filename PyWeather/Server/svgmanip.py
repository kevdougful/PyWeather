'''
Provides tools for using applying data from a Forecast object
to an SVG template.
'''
import codecs

def write_forecast(forecast_obj):
    '''
    Writes a Forecast object using template.svg
    '''
    # Open the SVG template (read-only)
    output = codecs.open('./template.svg', 'r', encoding='utf-8').read()
    for day in forecast_obj.ForecastDays:
        output = write_forecastday(output, day)
    codecs.open('forecast.svg', 'w', encoding='utf-8').write(output)

def write_forecastday(svg, forecastday_obj):
    '''
    Writes a ForecastDay object to the given svg object
    '''
    period = forecastday_obj.period

    # Icons
    svg = svg.replace('P' + period + 'I1', forecastday_obj.day_icon)
    svg = svg.replace('P' + period + 'I2', forecastday_obj.night_icon)

    period = 'period' + period

    # Text
    svg = svg.replace(period + 'title', forecastday_obj.date.strftime('%a %b-%d'))
    svg = svg.replace(period + 'daytext1', _parse_text(forecastday_obj.daytext)[0])
    svg = svg.replace(period + 'daytext2', _parse_text(forecastday_obj.daytext)[1])
    svg = svg.replace(period + 'nighttext1', _parse_text(forecastday_obj.nighttext)[0])
    svg = svg.replace(period + 'nighttext2', _parse_text(forecastday_obj.nighttext)[1])

    # High, low, humidity
    svg = svg.replace(period + 'high', str(forecastday_obj.high_F) + 'F')
    svg = svg.replace(period + 'low', str(forecastday_obj.low_F) + 'F')
    svg = svg.replace(period + 'humidity', str(forecastday_obj.humidity) + '%')

    # Rain info
    svg = svg.replace(period + 'dayrainchance', str(forecastday_obj.daypop) + '%')
    svg = svg.replace(period + 'nightrainchance', str(forecastday_obj.nightpop) + '%')
    svg = svg.replace(period + 'dayrainamount', str(forecastday_obj.qpf_day_in) + '\"')
    svg = svg.replace(period + 'nightrainamount', str(forecastday_obj.qpf_night_in) + '\"')
    return svg

def _parse_text(text):
    '''
    Parses forecast text: removes Low/High and Wind info
    '''
    new_end = text.find('High')
    if new_end == -1:
        new_end = text.find('Low')
    if new_end > -1:
        text = text[:new_end - 1]
    return _wrap_text(text)

def _wrap_text(text):
    '''
    Splits a long line of text into two lines
    '''
    breaklength = 30
    wrapped_text = ['', '']
    if len(text) <= breaklength:
        # Don't wrap short strings
        wrapped_text[0] = text
    else:
        br = text.find(' ', breaklength)
        wrapped_text[0] = text[:br]
        wrapped_text[1] = text[br:]
    return wrapped_text