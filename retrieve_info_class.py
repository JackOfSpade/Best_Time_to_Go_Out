import configparser
import requests
import sys
import json
import time
import datetime


class retrieve_info:
    """
    This class retrieves weather information.
    """

    # uses the configparser standard library to read the INI file.
    @staticmethod
    def get_accuweather_api_key():
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config["weather_api_keys"]["accuweather_api_key"]

    @staticmethod
    def get_location_key(api_key, postal_or_zip_code):
        # order of query strings doesn't matter
        url = "http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey=%s&q=%s" % (api_key, postal_or_zip_code)

        # get raw response string and convert to json
        response = requests.get(url).json()
        return response[0]["Key"]

    @staticmethod
    def get_hourly_weather_json(location_key, api_key, metric):
        url = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/%s?apikey=%s&details=true&metric=%s" % (location_key, api_key, metric)
        response = requests.get(url).json()
        return response
