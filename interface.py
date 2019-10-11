import json
import retrieve_info_class
import hourly_weather_class
import datetime
import tkinter



def main():
    accuweather_api_key = retrieve_info_class.retrieve_info.get_accuweather_api_key()
    postal_or_zip_code = "M1P3G4"
    # location_key = get_location_key(accuweather_api_key, postal_or_zip_code)
    location_key = "48968_PC"
    # Make this configurable
    metric = "true"

    hourly_weather_instance_list = retrieve_info_class.retrieve_info.get_hourly_weather(location_key, accuweather_api_key, metric)

    # For testing purposes
    for instance in hourly_weather_instance_list:
        if hourly_weather_class.hourly_weather.sunrise_time != None:
            print("Sunrise: " + hourly_weather_class.hourly_weather.sunrise_time)

        if hourly_weather_class.hourly_weather.sunset_time != None:
            print("Sunset: " + hourly_weather_class.hourly_weather.sunset_time)

        print("Time: " + hourly_weather_class.hourly_weather.time_tuple_to_string(*instance.time_tuple))
        print("Real-Feel Temperature: " + str(instance.real_feel_temperature_tuple[0]) + str(
            instance.real_feel_temperature_tuple[1]))
        print("Precipitation Probability: " + str(instance.precipitation_probability))
        print("UV Index: " + str(instance.uv_index))
        print("\n")

    print(" ------------------------------------------------------------------------------------------------------------ \n")

    retrieve_info_class.retrieve_info.remove_incompatible_hourly_weather(hourly_weather_instance_list)

    # For testing purposes
    for instance in hourly_weather_instance_list:
        if hourly_weather_class.hourly_weather.sunrise_time != None:
            print("Sunrise: " + hourly_weather_class.hourly_weather.sunrise_time)

        if hourly_weather_class.hourly_weather.sunset_time != None:
            print("Sunset: " + hourly_weather_class.hourly_weather.sunset_time)

        print("Time: " + hourly_weather_class.hourly_weather.time_tuple_to_string(*instance.time_tuple))
        print("Real-Feel Temperature: " + str(instance.real_feel_temperature_tuple[0]) + str(instance.real_feel_temperature_tuple[1]))
        print("Precipitation Probability: " + str(instance.precipitation_probability))
        print("UV Index: " + str(instance.uv_index))
        print("\n")

    print(" ------------------------------------------------------------------------------------------------------------ \n")

    retrieve_info_class.retrieve_info.group_compatible_hourly_weather(hourly_weather_instance_list)

    # For testing purposes:
    for element in hourly_weather_instance_list:
        if type(element) is hourly_weather_class.hourly_weather:
            if element.twenty_four_hour_time.hour == 23:
                next_hour = element.twenty_four_hour_time.hour.replace(hour = 0)
            else:
                next_hour = element.twenty_four_hour_time.replace(hour = element.twenty_four_hour_time.hour + 1)

            print("Time: " + hourly_weather_class.hourly_weather.time_tuple_to_string(*element.time_tuple) + " to " + hourly_weather_class.hourly_weather.time_tuple_to_string(hourly_weather_class.hourly_weather.convert_from_24_to_12_hour_time(next_hour)))
        elif type(element) is tuple:
            print("Time: " + hourly_weather_class.hourly_weather.time_tuple_to_string(*element[0].time_tuple) + " to " + hourly_weather_class.hourly_weather.time_tuple_to_string(*element[len(element) - 1].time_tuple))


if __name__ == "__main__":
    main()