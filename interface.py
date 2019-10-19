import tkinter
from ctypes import windll
import hourly_weather_class
import retrieve_info_class
import os

location_name = None
label_list = []
entry_box = None

def get_appropriate_hourly_weather_instance_list(metric, exercise_type, postal_or_zip_code):
    global location_name
    accuweather_api_key = retrieve_info_class.retrieve_info.get_accuweather_api_key(0)
    # Revert after testing:
    location = retrieve_info_class.retrieve_info.get_location(accuweather_api_key, postal_or_zip_code)

    if location is not None:
        location_name = location[0]
        location_key = location[1]
        # location_key = "48968_PC"

        # Get hourly weather data for TODAY.
        hourly_weather_instance_list = retrieve_info_class.retrieve_info.get_hourly_weather(location_key,
                                                                                            accuweather_api_key, metric)

        # For testing purposes
        # PyCharm Interface console fake-clear ------------
        print('\n' * 80)  # prints 80 line breaks
        os.system('cls' if os.name == 'nt' else 'clear')
        # --------------------------------------------------
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

        retrieve_info_class.retrieve_info.remove_incompatible_hourly_weather(hourly_weather_instance_list,
                                                                             exercise_type)
        retrieve_info_class.retrieve_info.group_compatible_hourly_weather(hourly_weather_instance_list)

        return hourly_weather_instance_list
    else:
        return None



def interface():
    global entry_box

    # Improve DPI Sharpness
    windll.shcore.SetProcessDpiAwareness(1)
    root = tkinter.Tk()
    root.title("Best Time to Go Out")

    # Add a grid
    mainframe = tkinter.Frame(root)
    mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1,)
    mainframe.pack(pady=100, padx=100)

    # Create a Tkinter variable
    unit_type = tkinter.StringVar(root)

    # set to the used in the drop down.
    unit_type_choices = ["Imperial", "Metric"]
    # set the default option
    unit_type.set("Imperial")

    unit_type_option_menu = tkinter.OptionMenu(mainframe, unit_type, *unit_type_choices)
    unit_type_option_menu.config(font="Calibri 12")
    unit_type_option_menu.grid(row=1, column=2)
    # Change menu option font
    mainframe.nametowidget(unit_type_option_menu.menuname).configure(font="Calibri 12")

    exercise_type = tkinter.StringVar(root)
    exercise_type_choices = ["Walking", "Jogging", "Cycling"]
    exercise_type.set("Walking")
    exercise_type_option_menu = tkinter.OptionMenu(mainframe, exercise_type, *exercise_type_choices)
    exercise_type_option_menu.config(font="Calibri 12")
    exercise_type_option_menu.grid(row=0, column=2)
    mainframe.nametowidget(exercise_type_option_menu.menuname).configure(font="Calibri 12")

    tkinter.Label(mainframe, text="Type of Exercise:", font="Calibri 12 bold").grid(row=0, column=1, padx=20, pady=10)
    tkinter.Label(mainframe, text="Unit Type:", font="Calibri 12 bold").grid(row=1, column=1, padx=20, pady=10)
    tkinter.Label(mainframe, text="Zip/Postal Code:", font="Calibri 12 bold").grid(row=2, column=1, padx=20, pady=10)

    entry_box = tkinter.Entry(mainframe, fg="#D3D3D3", font="Calibri 12 bold")
    entry_box.insert(0, "90210")
    entry_box.grid(row=2, column=2, padx=20, pady=10)
    entry_box.bind("<FocusIn>", lambda arg: (entry_box.delete(0, tkinter.END), entry_box.config(fg="black", font="Calibri 12")))
    entry_box.bind("<Return>", lambda arg: (change_interface(unit_type.get(), exercise_type.get(), entry_box.get(), mainframe),))

    button = tkinter.Button(mainframe, text="OK", command=lambda: (change_interface(unit_type.get(), exercise_type.get(), entry_box.get(), mainframe),), font="Calibri 12")
    button.grid(row=3, column=2, padx=20, pady=10)

    root.mainloop()

def extract_data(hourly_weather_instance_list):
    # 2D array, each element is [time_interval, feels-like_temperature_tuple_list, uv_index_list]
    data_list = []

    for element in hourly_weather_instance_list:
        temp_list = []

        if len(element) == 1:
            if element[0].twenty_four_hour_time.hour == 23:
                next_hour = element[0].twenty_four_hour_time.replace(hour=0)
            else:
                next_hour = element[0].twenty_four_hour_time.replace(hour=element[0].twenty_four_hour_time.hour + 1)

            temp_list.append(hourly_weather_class.hourly_weather.time_tuple_to_string(*element[0].time_tuple) + " - " + hourly_weather_class.hourly_weather.time_tuple_to_string(*hourly_weather_class.hourly_weather.convert_from_24_to_12_hour_time(next_hour)))
            temp_list.append(element[0].real_feel_temperature_tuple)
            temp_list.append(element[0].uv_index)

            data_list.append(temp_list)
        elif len(element) > 1:
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
        temp_list = []

        if type(element[1]) is list:
            for item in element[1]:
                temp_list.append(item[0])

            unit_type = element[1][0][1]
        elif type(element[1]) is tuple:
            temp_list.append(element[1][0])
            unit_type = element[1][1]

        minimum = min(temp_list)
        maximum = max(temp_list)


        if minimum == maximum:
            element[1] = str(minimum) + unit_type
        else:
            element[1] = str(minimum) + " " + unit_type + " - " + str(maximum) + " " + unit_type

        temp_list.clear()

        if type(element[2]) is list:
            temp_list += element[2]
        elif type(element[2]) is int:
            temp_list.append(element[2])


        minimum = min(temp_list)
        maximum = max(temp_list)

        if minimum == maximum:
            element[2] = str(minimum)
        else:
            element[2] = str(minimum) + " - " + str(maximum)
    return data_list

def clear_all_data_labels():
    global label_list

    for element in label_list:
            element.destroy()

    label_list.clear()

def change_interface(unit_type, exercise_type, postal_or_zip_code, mainframe):
    global location_name
    global label_list
    global entry_box

    entry_box.bind("<FocusIn>", lambda arg: entry_box.config(fg="black", font="Calibri 12"))

    if unit_type == "Imperial":
        metric = "false"
    else:
        metric = "true"

    tuples_of_hourly_weather_instances_list = get_appropriate_hourly_weather_instance_list(metric, exercise_type, postal_or_zip_code)
    if tuples_of_hourly_weather_instances_list is not None:
        if len(tuples_of_hourly_weather_instances_list) > 0:
            clear_all_data_labels()

            data_list = extract_data(tuples_of_hourly_weather_instances_list)

            temp_label = tkinter.Label(mainframe, text="Best Time to Go Out in " + location_name + ":", font="Calibri 14 bold")
            temp_label.grid(row=4, column=1, padx=20, pady=(100, 10))
            label_list.append(temp_label)

            temp_label = tkinter.Label(mainframe, text="Feels-like Temperature Range:", font="Calibri 14 bold")
            temp_label.grid(row=5, column=1, padx=20, pady=10)
            label_list.append(temp_label)

            temp_label = tkinter.Label(mainframe, text="UV Index Range:", font="Calibri 14 bold")
            temp_label.grid(row=6, column=1, padx=20, pady=10)
            label_list.append(temp_label)

            row = 4
            column = 2
            length = len(data_list)
            while column - 2 < length:
                temp_label = tkinter.Label(mainframe, text=data_list[column - 2][0], font="Calibri 14")
                temp_label.grid(row=row, column=column, padx=20, pady=(100, 10))
                label_list.append(temp_label)

                temp_label = tkinter.Label(mainframe, text=data_list[column - 2][1], font="Calibri 14")
                temp_label.grid(row=row + 1, column=column, padx=20, pady=10)
                label_list.append(temp_label)

                temp_label = tkinter.Label(mainframe, text=data_list[column - 2][2], font="Calibri 14")
                temp_label.grid(row=row + 2, column=column, padx=20, pady=10)
                label_list.append(temp_label)

                column += 1

            if tuples_of_hourly_weather_instances_list[0][0].sunrise_time is not None:
                temp_label = tkinter.Label(mainframe, text="Sunrise at " + tuples_of_hourly_weather_instances_list[0][0].sunrise_time, font="Calibri 14")
                temp_label.grid(row=row + 3, column=1, padx=20, pady=10)
                label_list.append(temp_label)

            if tuples_of_hourly_weather_instances_list[0][0].sunset_time is not None:
                temp_label = tkinter.Label(mainframe, text="Sunset at " + tuples_of_hourly_weather_instances_list[0][0].sunset_time, font="Calibri 14")
                temp_label.grid(row=row + 4, column=1, padx=20, pady=10)
                label_list.append(temp_label)
        else:
            clear_all_data_labels()
            temp_label = tkinter.Label(mainframe, text="Weather is bad in " + location_name + " for the rest of the day.\n" + exercise_type + " is not recommended.\nDrive instead or try a different exercise.", font="Calibri 14")
            temp_label.grid(row=4, column=1, padx=20, pady=(100, 10))
            label_list.append(temp_label)
    else:
        clear_all_data_labels()

if __name__ == "__main__":
    interface()
