import json
import retrieve_info_class
import hourly_weather_class
import datetime
import tkinter
import plotly.graph_objects as graph_objects


def get_appropriate_hourly_weather_instance_list(metric, postal_or_zip_code):
    accuweather_api_key = retrieve_info_class.retrieve_info.get_accuweather_api_key()
    # location_key = retrieve_info_class.retrieve_info.get_location_key(accuweather_api_key, postal_or_zip_code)
    # Revert after testing:
    location_key = "48968_PC"
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

    retrieve_info_class.retrieve_info.group_compatible_hourly_weather(hourly_weather_instance_list)

    return hourly_weather_instance_list

def interface():
    root = tkinter.Tk()
    root.title("Best Time to Jog?")

    # Add a grid
    mainframe = tkinter.Frame(root)
    mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1,)
    mainframe.pack(pady=100, padx=100)

    # Create a Tkinter variable
    tkvar = tkinter.StringVar(root)

    # set to the used in the drop down.
    choices = {"Imperial", "Metric"}
    # set the default option
    tkvar.set("Imperial")

    popup_menu = tkinter.OptionMenu(mainframe, tkvar, *choices)
    tkinter.Label(mainframe, text="Choose a unit type:").grid(row=1, column=1)
    popup_menu.grid(row=2, column=1)

    entry_box = tkinter.Entry(mainframe, fg="grey")
    entry_box.insert(0, "Postal Code")
    entry_box.grid(row=3, column=1)
    entry_box.bind("<FocusIn>", lambda arg: (entry_box.delete(0, tkinter.END), entry_box.config(fg='black')))
    entry_box.bind("<FocusOut>", lambda arg: (entry_box.delete(0, tkinter.END), entry_box.config(fg='grey'), entry_box.insert(0, "Example: Joe Bloggs")))
    entry_box.bind("<Return>", lambda arg: (main(tkvar.get(), entry_box.get(), mainframe), ))

    button = tkinter.Button(mainframe, text="OK", command=lambda: (main(tkvar.get(), entry_box.get(), mainframe), ))
    button.grid(row=4, column=1)

    root.mainloop()

def extract_data(hourly_weather_instance_list):
    # 2D array, each element is [time_interval, feels-like_temperature_tuple_list, uv_index_list]
    data_list = []

    for element in hourly_weather_instance_list:
        if type(element) is hourly_weather_class.hourly_weather:
            data_list[hourly_weather_instance_list.index(element)] = []

            if element.twenty_four_hour_time.hour == 23:
                next_hour = element.twenty_four_hour_time.hour.replace(hour=0)
            else:
                next_hour = element.twenty_four_hour_time.replace(hour=element.twenty_four_hour_time.hour + 1)

            data_list[hourly_weather_instance_list.index(element)][0] = hourly_weather_class.hourly_weather.time_tuple_to_string(*element.time_tuple) + " - " + hourly_weather_class.hourly_weather.time_tuple_to_string(hourly_weather_class.hourly_weather.convert_from_24_to_12_hour_time(next_hour))
            data_list[hourly_weather_instance_list.index(element)][1] = element.real_feel_temperature_tuple
            data_list[hourly_weather_instance_list.index(element)][2] = element.uv_index
        elif type(element) is tuple:
            data_list[hourly_weather_instance_list.index(element)] = []
            data_list[hourly_weather_instance_list.index(element)][1] = []
            data_list[hourly_weather_instance_list.index(element)][2] = []

            data_list[hourly_weather_instance_list.index(element)][0] = hourly_weather_class.hourly_weather.time_tuple_to_string(*element[0].time_tuple) + " - " + hourly_weather_class.hourly_weather.time_tuple_to_string(*element[len(element) - 1].time_tuple)

            for item in element:
                data_list[hourly_weather_instance_list.index(element)][1].append(item.real_feel_temperature_tuple)
                data_list[hourly_weather_instance_list.index(element)][2].append(item.uv_index)

    return data_list

def main(option_menu_value, postal_or_zip_code, mainframe):
    if option_menu_value == "Imperial":
        metric = "false"
    else:
        metric = "true"

    hourly_weather_instance_list = get_appropriate_hourly_weather_instance_list(metric, postal_or_zip_code)
    header_column1_list = ["Best Time to Jog"]
    header_dictionary = dict()
    header_dictionary["values"] = [header_column1_list]
    header_dictionary["values"] = header_dictionary["values"] + extract_time_intervals(hourly_weather_instance_list)

    cell_column1_list = ["Feels-like Temperature Range", "UV Index Range"]
    cell_column2_list = [95, 85]
    cell_column3_list = [101, 102]

    cell_dictionary = dict()
    cell_dictionary["values"] = [cell_column1_list, cell_column2_list, cell_column3_list]

    table = graph_objects.Figure(data=[graph_objects.Table(header=header_dictionary, cells=cell_dictionary)])
    table.show()



if __name__ == "__main__":
    interface()
