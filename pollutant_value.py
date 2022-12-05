from datetime import datetime


class PollutantValue:
    def __init__(self, value, sensorID, timestamp, type):
        self.value = value
        self.sensorID = sensorID
        self.timestamp = timestamp
        self.type = type  # 0: NO2, 1: SO2, 2: PM10, 3:O3


if __name__ == "__main__":
    timestamp_input = datetime(
        year=2017, month=2, day=5, hour=13, minute=14, second=31)
    pollutant_data = PollutantValue(
        97.4554108125763, sensorID=4, timestamp=timestamp_input, type=1)
    print(pollutant_data.sensorID)
