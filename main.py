from data_handler import DataHandler
from datetime import datetime


def get_coordinates():
    valid_lat = False
    valid_long = False
    lat = 0
    long = 0
    while not valid_lat:
        try:
            lat = float(input("Enter Latitude: "))
            if lat < -90 or lat > 90:
                print("Invalid latitude!\n")
            else:
                valid_lat = True
        except ValueError:
            print("Invalid latitude!\n")
    while not valid_long:
        try:
            long = float(input("Enter Longitude: "))
            if long < -90 or long > 90:
                print("Invalid longitude!\n")
            else:
                valid_long = True
        except ValueError:
            print("Invalid longitude!\n")
    return lat, long


def get_timestamp(option):
    if not option:
        yr = int(input("Enter year (2017 - 2019): "))
        while yr < 2017 or yr > 2019:
            print("Invalid year!\n")
            yr = int(input("Enter year (2017 - 2019): "))
        mth = int(input("Enter month (1 - 12): "))
        while mth < 1 or mth > 12:
            print("Invalid month!")
            mth = int(input("Enter month (1 - 12): "))
        day = int(input("Enter day (1 - 31): "))
        while day < 1 or day > 31:
            print("Invalid day!\n")
            day = int(input("Enter day (1 - 31): "))
        hr = int(input("Enter hour (0 - 23): "))
        while hr < 0 or hr > 23:
            print("Invalid hour!\n")
            hr = int(input("Enter hour (0 - 23): "))
        minute = int(input("Enter min (0 - 59): "))
        while minute < 0 or minute > 59:
            print("Invalid minute!\n")
            minute = int(input("Enter min (0 - 59): "))
        query_timestamp = datetime(
            year=yr, month=mth, day=day, hour=hr, minute=minute)
        return query_timestamp
    else:
        print("Enter starting time:")
        query_timestamp_start = get_timestamp(False)
        print("Enter end time:")
        query_timestamp_end = get_timestamp(False)
        return query_timestamp_start, query_timestamp_end


def get_single_air_quality():
    lat, long = get_coordinates()
    coordinates = (lat, long)
    query_timestamp = get_timestamp(False)

    data_handler = DataHandler("test_data.csv")
    air_qualities = data_handler.get_air_quality(coordinates, query_timestamp)
    print("Your coordinates: ", coordinates, "\n")
    print("Your query timestamp: ", query_timestamp, "\n\n")
    if air_qualities[0] == -1:
        print("Error: No valid sensors within range of the specified coordinates")
    elif air_qualities[0] == -2:
        print("Error: No valid data within specified averaging timeframes contained in sensors")
    else:
        print("NO2 Air Quality: ", round(air_qualities[1][0]), "\n")
        print("SO2 Air Quality: ", round(air_qualities[1][1]), "\n")
        print("PM10 Air Quality: ", round(air_qualities[1][2]), "\n")
        print("O3 Air Quality: ", round(air_qualities[1][3]), "\n\n")
        print("Total Air Quality: ", round(air_qualities[0]), "\n\n")


def get_average_air_quality():
    lat, long = get_coordinates()
    coordinates = (lat, long)
    query_timestamp_start, query_timestamp_end = get_timestamp(True)

    data_handler = DataHandler("test_data.csv")
    air_qualities = data_handler.get_air_quality_timespan(coordinates, query_timestamp_start, query_timestamp_end)
    print("Your coordinates: ", coordinates, "\n")
    print("Your starting time: ", query_timestamp_start, "\n")
    print("Your ending time: ", query_timestamp_end, "\n")
    if air_qualities[0] == -1:
        print("Error: No valid sensors within range of the specified coordinates")
    elif air_qualities[0] == -2:
        print("Error: No valid data within specified averaging timeframes contained in sensors")
    else:
        print("NO2 Air Quality: ", round(air_qualities[1][0]), "\n")
        print("SO2 Air Quality: ", round(air_qualities[1][1]), "\n")
        print("PM10 Air Quality: ", round(air_qualities[1][2]), "\n")
        print("O3 Air Quality: ", round(air_qualities[1][3]), "\n\n")
        print("Total Air Quality: ", round(air_qualities[0]), "\n\n")


def get_similar_sensors():
    query_timestamp_start, query_timestamp_end = get_timestamp(True)
    valid_difference = False
    value_difference = 0
    while not valid_difference:
        try:
            value_difference = float(input("Enter the value difference to be considered \"Similar\" (0, infinity): "))
            if value_difference <= 0:
                print("Invalid value difference!\n")
            else:
                valid_difference = True
        except ValueError:
            print("Invalid value difference!\n")

    data_handler = DataHandler("test_data.csv")
    similar_sensors = data_handler.get_similar_sensors(query_timestamp_start, query_timestamp_end, value_difference)


if __name__ == "__main__":
    print("#################################################################")
    print("\tWelcome to Air Quality Management System")
    print("#################################################################")
    print("\n------------------")
    print("Mode selection:")
    print("1. Retrieve aqi at given coordinates at given time")
    print("2. Retrieve average aqi at given coordinates in given timespan")
    print("3. Find sensors with similar pollutant values in a given timespan")
    validMode = False
    mode = 0
    while not validMode:
        try:
            mode = int(input("Select a mode (1-3): "))
            if 1 <= mode <= 3:
                validMode = True
            else:
                print("Invalid mode!\n")
        except ValueError:
            print("Invalid mode!\n")
    if mode == 1:
        get_single_air_quality()
    elif mode == 2:
        get_average_air_quality()
    elif mode == 3:
        get_similar_sensors()
