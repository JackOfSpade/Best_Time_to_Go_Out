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
        temp_list = []

        if type(element) is hourly_weather_class.hourly_weather:
            if element.twenty_four_hour_time.hour == 23:
                next_hour = element.twenty_four_hour_time.hour.replace(hour=0)
            else:
                next_hour = element.twenty_four_hour_time.replace(hour=element.twenty_four_hour_time.hour + 1)

            temp_list.append(hourly_weather_class.hourly_weather.time_tuple_to_string(*element.time_tuple) + " - " + hourly_weather_class.hourly_weather.time_tuple_to_string(hourly_weather_class.hourly_weather.convert_from_24_to_12_hour_time(next_hour)))
            temp_list.append(element.real_feel_temperature_tuple)
            temp_list.append(element.uv_index)

            data_list.append(temp_list)
        elif type(element) is tuple:
            temp_list.append(hourly_weather_class.hourly_weather.time_tuple_to_string(*element[0].time_tuple) + " - " + hourly_weather_class.hourly_weather.time_tuple_to_string(*element[len(element) - 1].time_tuple))
            temp_list2 = []
            temp_list3 = []

            for item in element:
                temp_list2.append(item.real_feel_temperature_tuple)
                temp_list3.append(item.uv_index)

            temp_list.append(temp_list2)
            temp_list.append(temp_list3)

            data_list.append(temp_list)

        # Get min/max
    for element in data_list:

        minimum = min([x[0] for x in element[1]])
        maximum = max([x[0] for x in element[1]])

        if minimum == maximum:
            element[1] = [str(minimum) + str(element[1][data_list.index(element)][1])]
        else:
            element[1] = [str(minimum) + str(element[1][data_list.index(element)][1]) + " - " + str(maximum) + str(element[1][data_list.index(element)][1])]
                
        minimum = min(element[2])
        maximum = max(element[2])

        if minimum == maximum:
            element[2] = [str(minimum)]
        else:
            element[2] = [str(minimum) + " - " + str(maximum)]

        element[1].append(element[2])
        del element[2]
    return data_list

def main(option_menu_value, postal_or_zip_code, mainframe):
    if option_menu_value == "Imperial":
        metric = "false"
    else:
        metric = "true"

    hourly_weather_instance_list = get_appropriate_hourly_weather_instance_list(metric, postal_or_zip_code)
    data_list = extract_data(hourly_weather_instance_list)
    header_column1_list = ["Best Time to Jog"]
    header_dictionary = dict()
    header_dictionary["values"] = [header_column1_list]

    cell_column1_list = [["Feels-like Temperature", "UV Index"]]
    cell_dictionary = dict()
    cell_dictionary["values"] = cell_column1_list

    print(data_list)

    for element in data_list:
         header_dictionary["values"].append(element[0])
         cell_dictionary["values"].append(element[1])

    table = graph_objects.Figure(data=[graph_objects.Table(header=header_dictionary, cells=cell_dictionary)])
    table.show()



if __name__ == "__main__":
    interface()
