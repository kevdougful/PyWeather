import getxml
from forecastdata import Forecast

cast = Forecast('MO/Maryland_Heights')
for day in cast.ForecastDays:
    print(str(day))
    print(day.maxwind_dir)