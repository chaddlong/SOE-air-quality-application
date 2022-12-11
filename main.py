from data_handler import DataHandler
from datetime import datetime

if __name__ == "__main__":
    print("#################################################################")
    print("\tWelcome to Air Quality Management System")
    print("#################################################################")
    print("\n------------------")
    lat = float(input("Enter Latitude: "))
    while lat < -90 or lat > 90:
        print("Invalid latitude!\n")
        lat = float(input("Enter Latitude: "))
    long = float(input("Enter Longitude: "))
    while long < -90 or long > 90:
        print("Invalid longitude!\n")
        long = float(input("Enter Longitude: "))
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
    min = int(input("Enter min (0 - 59): "))
    while min < 0 or min > 59:
        print("Invalid minute!\n")
        min = int(input("Enter min (0 - 59): "))

    coordinates = (lat, long)
    timestamp_str = yr + mth + day + hr + min
    query_timestamp = datetime(
        year=yr, month=mth, day=day, hour=hr, minute=min)

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

