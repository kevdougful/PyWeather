"""Main entry point for PyWeather program.

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
#!/usr/bin/python

import apirequest
import forecastdata
import svgmanip

forecast = forecastdata.Forecast('MO/Maryland_Heights')
svgmanip.write_forecast(forecast)
f = open('radar.gif', 'wb')
params = '?width=800&height=400&newmaps=1&num=15&delay=25'
img = apirequest.radar_request('MO/Maryland_Heights', request_params=params)
f.write(img)
f.close()