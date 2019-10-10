import datetime


class hourly_weather:
    """
    This class contains weather information for 1 specific hour.
    """

    @staticmethod
    def convert_from_epoch_to_12_hour_time(epoch_time):
        twelve_hour_time = datetime.datetime.fromtimestamp(epoch_time)

        if twelve_hour_time.hour == 0:
            converted_hour = 12
            twelve_hour_time = twelve_hour_time.replace(hour=converted_hour, minute=twelve_hour_time.minute)
            period = "am"
        elif twelve_hour_time.hour == 12:
            period = "pm"
        elif twelve_hour_time.hour < 12:
            period = "am"
        else:
            converted_hour = twelve_hour_time.hour - 12
            twelve_hour_time = twelve_hour_time.replace(hour=converted_hour, minute=twelve_hour_time.minute)
            period = "pm"
        return (twelve_hour_time, period)

    @staticmethod
    def time_tuple_to_string(twelve_hour_time, period):
        if twelve_hour_time.minute == 0:
            return str(twelve_hour_time.hour) + ":" + str(twelve_hour_time.minute) + "0 " + period

        return str(twelve_hour_time.hour) + ":" + str(twelve_hour_time.minute) + " " + period

    sunrise_time = None
    sunset_time = None

    def __init__(self, time_tuple, real_feel_temperature_tuple, precipitation_probability, uv_index):
        # datetime object and period string
        self.time_tuple = time_tuple
        # temperature value and unit type
        self.real_feel_temperature_tuple = real_feel_temperature_tuple
        self.precipitation_probability = precipitation_probability
        self.uv_index = uv_index
