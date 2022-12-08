from data_handler import DataHandler
from datetime import datetime

if __name__ == "__main__":
    print("#################################################################")
    print("\tWelcome to Air Quality Management System")
    print("#################################################################")
    print("\n------------------")
    lat = float(input("Enter Latitude: "))
    long = float(input("Enter Longitude: "))

    yr = int(input("Enter year (2017 - 2019): "))
    mth = int(input("Enter month (0 - 12): "))
    day = int(input("Enter day (0 - 31): "))
    hr = int(input("Enter hour (0 - 24): "))
    min = int(input("Enter min (0 - 60): "))

    coordinates = (lat, long)
    timestamp_str = yr + mth + day + hr + min
    query_timestamp = datetime(
        year=yr, month=mth, day=day, hour=hr, minute=min)

    data_handler = DataHandler("test_data.csv")
    air_qualities = data_handler.get_air_quality(coordinates, query_timestamp)
    print("Your coordinates: ", coordinates, "\n")
    print("Your query timestamp: ", query_timestamp, "\n\n")
    print("NO2 Air Quality: ", round(air_qualities[1][0], 2), "\n")
    print("SO2 Air Quality: ", round(air_qualities[1][1], 2), "\n")
    print("PM10 Air Quality: ", round(air_qualities[1][2], 2), "\n")
    print("O3 Air Quality: ", round(air_qualities[1][3], 2), "\n\n")
    print("Total Air Quality: ", round(air_qualities[0], 2), "\n\n")

