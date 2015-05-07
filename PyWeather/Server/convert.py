"""Provides functions for performing various unit conversions.

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
"""
class Temperature(object):
    """Temperature conversion functions.
    """
    def f_to_c(fahrenheit):
        """Converts fahrenheit to celsius.

        Args:
            fahrenheit: fahrenheit value to convert to celsius.

        Returns:
            celsius value.
        """
        return (fahrenheit - 32) * 5 / 9

    def c_to_f(celsius):
        """Converts celsius to fahrenheit.

        Args:
            celsius: celsius value to convert to fahrenheit.

        Returns:
            fahrenheit value.
        """
        return celsius * 9 / 5 + 32