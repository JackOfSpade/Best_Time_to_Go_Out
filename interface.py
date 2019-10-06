import json
import retrieve_info_class
import hourly_weather_class


def main():
    accuweather_api_key = retrieve_info_class.retrieve_info.get_accuweather_api_key()
    postal_or_zip_code = "M1P3G4"
    # location_key = get_location_key(accuweather_api_key, postal_or_zip_code)
    location_key = "48968_PC"
    metric = "true"

    hourly_weather_instance_list = retrieve_info_class.retrieve_info.get_hourly_weather(location_key, accuweather_api_key, metric)

    # USE IsDayLight to determine sunrise/sunset time



    # For debugging purposes
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

if __name__ == "__main__":
    main()