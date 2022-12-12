from data_handler import DataHandler
from datetime import datetime

query_timestamp_start = datetime(year=2017, month=1, day=1, hour=0, minute=1)
query_timestamp_end = datetime(year=2017, month=1, day=1, hour=2, minute=59)
data_handler = DataHandler("test_data.csv")
air_qualities = data_handler.get_similar_sensors(
    query_timestamp_start, query_timestamp_end)
print(air_qualities)
