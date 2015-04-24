'''
convert.py

This module contains functions for various unit conversions
'''
class temperature(object):
    '''
    temperature conversion functions
    '''
    # convert fahrenheit to celsius
    def f_to_c(fahrenheit):
        return (fahrenheit - 32) * 5 / 9

    # convert celsius to fahrenheit
    def c_to_f(celsius):
        return celsius * 9 / 5 + 32