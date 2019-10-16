import datetime
import copy

class hourly_weather:
    """
    This class contains weather information for 1 specific hour.
    """

    @staticmethod
    def convert_from_epoch_to_12_hour_time(epoch_time):
        twenty_four_hour_time = datetime.datetime.fromtimestamp(epoch_time)
        twelve_hour_time = copy.deepcopy(twenty_four_hour_time)

        if twenty_four_hour_time.hour == 0:
            converted_hour = 12
            twelve_hour_time = twenty_four_hour_time.replace(hour=converted_hour)
            period = "am"
        elif twenty_four_hour_time.hour == 12:
            period = "pm"
        elif twenty_four_hour_time.hour < 12:
            period = "am"
        elif twenty_four_hour_time.hour > 12:
            converted_hour = twenty_four_hour_time.hour - 12
            twelve_hour_time = twenty_four_hour_time.replace(hour=converted_hour)
            period = "pm"

        return (twelve_hour_time, period, twenty_four_hour_time)

    @staticmethod
    def time_tuple_to_string(twelve_hour_time, period):
        if twelve_hour_time.minute == 0:
            return str(twelve_hour_time.hour) + ":" + str(twelve_hour_time.minute) + "0 " + period

        return str(twelve_hour_time.hour) + ":" + str(twelve_hour_time.minute) + " " + period

    @staticmethod
    def convert_from_24_to_12_hour_time(twenty_four_hour_time):
        twelve_hour_time = copy.deepcopy(twenty_four_hour_time)

        if twenty_four_hour_time.hour == 0:
            converted_hour = 12
            twelve_hour_time = twenty_four_hour_time.replace(hour=converted_hour)
            period = "am"
        elif twenty_four_hour_time.hour == 12:
            period = "pm"
        elif twenty_four_hour_time.hour < 12:
            period = "am"
        elif twenty_four_hour_time.hour > 12:
            converted_hour = twenty_four_hour_time.hour - 12
            twelve_hour_time = twenty_four_hour_time.replace(hour=converted_hour)
            period = "pm"
        return (twelve_hour_time, period)

    # @staticmethod
    # def convert_from_12_to_24_hour_time(twelve_hour_time):
    #     if twenty_four_hour_time.hour == 23:
    #         next_hour = element.twenty_four_hour_time.hour.replace(hour=0)
    #     else:
    #         next_hour = element.twenty_four_hour_time.replace(hour=element.twenty_four_hour_time.hour + 1)

    sunrise_time = None
    sunset_time = None

    def __init__(self, time_tuple, twenty_four_hour_time, real_feel_temperature_tuple, precipitation_probability, uv_index):
        # datetime object and period string
        self.time_tuple = time_tuple
        self.twenty_four_hour_time = twenty_four_hour_time
        # temperature value and unit type
        self.real_feel_temperature_tuple = real_feel_temperature_tuple
        self.precipitation_probability = precipitation_probability
        self.uv_index = uv_index
