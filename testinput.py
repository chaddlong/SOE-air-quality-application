from data_handler import DataHandler
from datetime import datetime

coordinates = (-8.157, -34.769)
query_timestamp = datetime(year=2017, month=1, day=1, hour=0, minute=2)
data_handler = DataHandler("test_data.csv")
air_qualities = data_handler.get_air_quality(coordinates, query_timestamp)
print("Your coordinates: ", coordinates, "\n")
print("Your query timestamp: ", query_timestamp, "\n\n")
print("NO2 Air Quality: ", round(air_qualities[1][0], 2), "\n")
print("SO2 Air Quality: ", round(air_qualities[1][1], 2), "\n")
print("PM10 Air Quality: ", round(air_qualities[1][2], 2), "\n")
print("O3 Air Quality: ", round(air_qualities[1][3], 2), "\n\n")
print("Total Air Quality: ", round(air_qualities[0], 2), "\n\n")