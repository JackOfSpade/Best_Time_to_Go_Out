import json
import retrieve_info_class
import hourly_weather_class


def main():
    accuweather_api_key = retrieve_info_class.retrieve_info.get_accuweather_api_key()
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
        element["EpochDateTime"] = hourly_weather_class.hourly_weather.convert_from_epoch_to_12_hour_time(element["EpochDateTime"])
        print(element)

if __name__ == "__main__":
    main()