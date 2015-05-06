'''
Provides tools for using applying data from a Forecast object
to an SVG template.
'''
import codecs

def write_forecast(forecast_obj):
    '''

    '''
    # Open the SVG template (read-only)
    output = codecs.open('./template.svg', 'r', encoding='utf-8').read()
    for day in forecast_obj.ForecastDays:
        output = write_forecastday(output, day)
    codecs.open('forecast.svg', 'w', encoding='utf-8').write(output)

def write_forecastday(svg, forecastday_obj):
    '''
    
    '''
    period = forecastday_obj.period

    # Icons
    svg = svg.replace('P' + period + 'I1', forecastday_obj.day_icon)
    svg = svg.replace('P' + period + 'I2', forecastday_obj.night_icon)

    period = 'period' + period

    # Text
    svg = svg.replace(period + 'title', forecastday_obj.date.strftime('%a %b-%d'))
    # TODO: strip out Low/high wind info from text 
    # TODO: parse day text into multiple lines
    svg = svg.replace(period + 'nighttext', forecastday_obj.nighttext)

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