import configparser
import requests
import sys
import json
import time
import datetime
import tkinter

import hourly_weather_class


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
    def get_hourly_weather(location_key, api_key, metric):
        # url = "http://dataservice.accuweather.com/forecasts/v1/hourly/24hour/%s?apikey=%s&details=true&metric=%s" % (location_key, api_key, metric)

        # Save a local copy in case internet fails.
        # with open("weather_list.txt", "w") as file_out:
        #    try:
        #        json.dump(requests.get(url).json(), file_out)
        #    except requests.exceptions.RequestException as e:
        #        print(e)
        #        tkinter.messagebox.showerror("Cannot connect to the weather API.\nPreviously saved weather data will be used.", "Error")

        with open("weather_list.txt") as file:
            weather_list = json.load(file)

        hourly_weather_instance_list = []
        previous_daylight = weather_list[0]["IsDaylight"]

        for dictionary in weather_list:
            time_tuple = hourly_weather_class.hourly_weather.convert_from_epoch_to_12_hour_time(dictionary["EpochDateTime"])
            real_feel_temperature_tuple = (dictionary["RealFeelTemperature"]["Value"], dictionary["RealFeelTemperature"]["Unit"])
            precipitation_probability = dictionary["PrecipitationProbability"]
            uv_index = dictionary["UVIndex"]
            hourly_weather_instance = hourly_weather_class.hourly_weather(time_tuple, real_feel_temperature_tuple, precipitation_probability, uv_index)

            # Find sunrise or sunset if not too late.
            previous_hour_plus_30_minutes = time_tuple[0].replace(hour = time_tuple[0].hour - 1, minute = 30)

            if not previous_daylight and dictionary["IsDaylight"]:
                hourly_weather_class.hourly_weather.sunrise_time = hourly_weather_class.hourly_weather.time_tuple_to_string(previous_hour_plus_30_minutes, time_tuple[1])
            elif previous_daylight and not dictionary["IsDaylight"]:
                hourly_weather_class.hourly_weather.sunset_time = hourly_weather_class.hourly_weather.time_tuple_to_string(previous_hour_plus_30_minutes, time_tuple[1])

            # Limit weather data to today.
            if time_tuple[1] == "am" and previous_period == "pm":
                break
            else:
                previous_period = time_tuple[1]
                previous_daylight = dictionary["IsDaylight"]
                hourly_weather_instance_list.append(hourly_weather_instance)

        return hourly_weather_instance_list