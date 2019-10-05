import datetime


class hourly_weather:
    """
    This class contains weather information for 1 specific hour.
    """

    @staticmethod
    def convert_from_epoch_to_12_hour_time(epoch_time):
        twelve_hour_time = datetime.datetime.fromtimestamp(epoch_time)

        if twelve_hour_time.hour < 12:
            period = "am"
        elif twelve_hour_time.hour == 12:
            period = "pm"
        else:
            converted_hour = twelve_hour_time.hour - 12
            twelve_hour_time = twelve_hour_time.replace(hour=converted_hour, minute=twelve_hour_time.minute)
            period = "pm"
        return (twelve_hour_time, period)

    @staticmethod
    def print_time_tuple(self, twelve_hour_time, period):
        if twelve_hour_time.minute == 0:
            return str(twelve_hour_time.hour) + ":" + str(twelve_hour_time.minute) + "0 " + period

        return str(twelve_hour_time.hour) + ":" + str(twelve_hour_time.minute) + " " + period

    sunrise_time = None
    sunset_time = None

    def __init__(self, ):
        self.time_tuple = None
        self.real_feel_temperature = None
        self.uv_index = None
        self.precipitation_probability = None