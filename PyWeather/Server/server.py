#!/usr/bin/python

import getxml
import forecastdata
import svgmanip

forecast = forecastdata.Forecast('MO/Maryland_Heights')
svgmanip.write_forecast(forecast)