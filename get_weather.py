import configparser
import requests
import sys
import json
import time
import datetime

# uses the configparser standard library to read the INI file.
def get_accuweather_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["weather_api_keys"]["accuweather_api_key"]


def get_open_weather_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["weather_api_keys"]["open_weather_api_key"]


def get_location_key(api_key, postal_or_zip_code):
    # order of query strings doesn't matter
    url = "http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey=%s&q=%s" % (api_key, postal_or_zip_code)

    # get raw response string and convert to json
    response = requests.get(url).json()
    return response[0]["Key"]


def get_weather(location_key, api_key, metric):
    url = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/%s?apikey=%s&details=true&metric=%s" % (location_key, api_key, metric)
    response = requests.get(url).json()
    return response


def convert_from_epoch_to_12_hour_time(epoch_time):
    twelve_hour_time = datetime.datetime.fromtimestamp(epoch_time)

    if twelve_hour_time.hour < 12:
        period = "am"
    elif twelve_hour_time.hour == 12:
        period = "pm"
    else:
        converted_hour = twelve_hour_time.hour - 12
        twelve_hour_time = twelve_hour_time.replace(hour = converted_hour, minute = twelve_hour_time.minute)
        period = "pm"

    if twelve_hour_time.minute == 0:
        return str(twelve_hour_time.hour) + ":" + str(twelve_hour_time.minute) + "0 " + period

    return str(twelve_hour_time.hour) + ":" + str(twelve_hour_time.minute) + " " + period


def main():
    accuweather_api_key = get_accuweather_api_key()
    open_weather_api_key = get_open_weather_api_key()
    postal_or_zip_code = "M1P3G4"
    # location_key = get_location_key(accuweather_api_key, postal_or_zip_code)
    location_key = "48968_PC"
    metric = "true"
    # weather_json = get_weather(location_key, accuweather_api_key, metric)
    #
    # with open("weather_json.txt", "w") as file_out:
    #     json.dump(weather_json, file_out)

    with open("weather_json.txt") as json_file:
        weather_json = json.load(json_file)

    # USE IsDayLight to determine sunrise/sunset time
    # 7:18am
    # sunrise_time = convert_from_epoch_to_12_hour_time(weather_json["city"]["sunrise"])
    # sunset_time = convert_from_epoch_to_12_hour_time(weather_json["city"]["sunset"])
    # print("Sunrise: " + sunrise_time)
    # print("Sunset: " + sunset_time)

    for element in weather_json:
        element["EpochDateTime"] = convert_from_epoch_to_12_hour_time(element["EpochDateTime"])
        print(element)

if __name__ == "__main__":
    main()