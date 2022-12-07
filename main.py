# from data_handler import DataHandler
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

    # DataHandler.get_air_quality(coordinates, query_timestamp)
    print("Your coordinates: ", coordinates)
    print("Your query timestamp: ", query_timestamp)
