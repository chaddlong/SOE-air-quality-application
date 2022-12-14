from data_handler import DataHandler
from datetime import datetime

coordinates = (-8.157, -34.769)
query_timestamp_start = datetime(year=2017, month=1, day=1, hour=0, minute=1)
query_timestamp_end = datetime(year=2019, month=12, day=31, hour=23, minute=59)
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
