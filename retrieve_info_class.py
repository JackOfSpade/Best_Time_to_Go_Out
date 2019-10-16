import configparser
import json
import tkinter
import requests
import database_class
import hourly_weather_class
import ctypes


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
    def get_location(api_key, postal_or_zip_code):
        # order of query strings doesn't matter
        url = "http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey=%s&q=%s" % (api_key, postal_or_zip_code)

        # get raw response string and convert to json
        response = requests.get(url).json()

        try:
            return (response[0]["EnglishName"], response[0]["Key"])
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, "The zip/postal code you've entered is not supported.", "Oops!", 0)
            print(e)
            return None



    @staticmethod
    def get_hourly_weather(location_key, api_key, metric):
        # Upgraded API key needed for 24-hour hourly weather data
        url = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/%s?apikey=%s&details=true&metric=%s" % (location_key, api_key, metric)

        # Save a local copy to text file in case internet fails.
        # with open("weather_list.txt", "w") as file_out:
        #    try:
        #        json.dump(requests.get(url).json(), file_out)
        #    except requests.exceptions.RequestException as e:
        #        print(e)
        #        tkinter.messagebox.showerror("Cannot connect to the weather API.\nPreviously saved weather data will be used.", "Error")

        # Open weather data from text file
        # with open("weather_list.txt") as file:
        #    weather_list = json.load(file)

        # Revert after testing:
        # Save a local copy to shelve in case internet fails.
        try:
            database_class.database.add("weather", json.dumps(requests.get(url).json()))
        except requests.exceptions.RequestException as e:
            print(e)
            tkinter.messagebox.showerror("Cannot connect to the weather API.\nPreviously saved weather data will be used.", "Error")

        # Open weather data from database
        weather_list = json.loads(database_class.database.access("weather"))

        hourly_weather_instance_list = []
        previous_daylight = weather_list[0]["IsDaylight"]
        previous_period = ""

        for dictionary in weather_list:
            temp_time_tuple = hourly_weather_class.hourly_weather.convert_from_epoch_to_12_hour_time(dictionary["EpochDateTime"])
            time_tuple = (temp_time_tuple[0], temp_time_tuple[1])
            twenty_four_hour_time = temp_time_tuple[2]
            real_feel_temperature_tuple = (dictionary["RealFeelTemperature"]["Value"], dictionary["RealFeelTemperature"]["Unit"])
            precipitation_probability = dictionary["PrecipitationProbability"]
            uv_index = dictionary["UVIndex"]
            hourly_weather_instance = hourly_weather_class.hourly_weather(time_tuple, twenty_four_hour_time, real_feel_temperature_tuple, precipitation_probability, uv_index)

            # Find sunrise or sunset if not too late.
            # Sunrise/sunset in North America will never cross am/pm
            previous_hour_plus_30_minutes = time_tuple[0].replace(hour=time_tuple[0].hour - 1, minute=30)

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

    @staticmethod
    # 8C to 23C
    def remove_incompatible_hourly_weather(hourly_weather_instance_list, exercise_type):
        lower_bound_metric = 0
        upper_bound_metric = 0
        lower_bound_imperial = 0
        upper_bound_imperial = 0

        if exercise_type == "Walking":
            lower_bound_metric = 12
            upper_bound_metric = 24
            lower_bound_imperial = 53.6
            upper_bound_imperial = 75.2
        elif exercise_type == "Running":
            lower_bound_metric = 8
            upper_bound_metric = 20
            lower_bound_imperial = 46.4
            upper_bound_imperial = 68
        elif exercise_type == "Cycling":
            lower_bound_metric = 15
            upper_bound_metric = 27
            lower_bound_imperial = 59
            upper_bound_imperial = 80.6

        # For testing purposes:
        # print("lower_bound_metric: " + str(lower_bound_metric))
        # print("upper_bound_metric: " + str(upper_bound_metric))
        # print("lower_bound_imperial: " + str(lower_bound_imperial))
        # print("upper_bound_imperial : " + str(upper_bound_imperial))

        i = 0
        length = len(hourly_weather_instance_list)
        while i < length:
            if (hourly_weather_instance_list[i].real_feel_temperature_tuple[1] == "C" and (hourly_weather_instance_list[i].real_feel_temperature_tuple[0] < lower_bound_metric or hourly_weather_instance_list[i].real_feel_temperature_tuple[0] > upper_bound_metric)) \
                    or \
                        (hourly_weather_instance_list[i].real_feel_temperature_tuple[1] == "F" and (hourly_weather_instance_list[i].real_feel_temperature_tuple[0] < lower_bound_imperial or hourly_weather_instance_list[i].real_feel_temperature_tuple[0] > upper_bound_imperial))\
                        or \
                            hourly_weather_instance_list[i].precipitation_probability > 0:
                hourly_weather_instance_list.remove(hourly_weather_instance_list[i])
                i -= 1
                length -= 1

            i += 1

    @staticmethod
    def group_compatible_hourly_weather(hourly_weather_instance_list):
        i = 0
        length = len(hourly_weather_instance_list)
        while i < length:
            if(i + 1 < length):
                if type(hourly_weather_instance_list[i]) is hourly_weather_class.hourly_weather:
                    if hourly_weather_instance_list[i + 1].twenty_four_hour_time.hour == (hourly_weather_instance_list[i].twenty_four_hour_time.hour + 1) \
                        or \
                            (hourly_weather_instance_list[i + 1].twenty_four_hour_time.hour == 0 and hourly_weather_instance_list[i].twenty_four_hour_time.hour == 23):
                        hourly_weather_instance_list[i] = (hourly_weather_instance_list[i], hourly_weather_instance_list[i+1])
                        hourly_weather_instance_list.remove(hourly_weather_instance_list[i+1])
                        i -= 1
                        length -= 1
                elif type(hourly_weather_instance_list[i]) is tuple:
                    if hourly_weather_instance_list[i + 1].twenty_four_hour_time.hour == (hourly_weather_instance_list[i][len(hourly_weather_instance_list[i]) - 1].twenty_four_hour_time.hour + 1) \
                         or \
                            (hourly_weather_instance_list[i + 1].twenty_four_hour_time.hour == 0 and hourly_weather_instance_list[i][len(hourly_weather_instance_list[i]) - 1].twenty_four_hour_time.hour == 23):
                        hourly_weather_instance_list[i] = hourly_weather_instance_list[i] + (hourly_weather_instance_list[i + 1],)
                        hourly_weather_instance_list.remove(hourly_weather_instance_list[i + 1])
                        i -= 1
                        length -= 1
            i += 1

