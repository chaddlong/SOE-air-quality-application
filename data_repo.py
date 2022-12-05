import csv
from datetime import datetime


class DataRepository:
    def __init__(self, csv_path):
        self.data = []  # PollutantValue
        self.setRawData(csv_path)

    def setRawData(self, csv_path):
        file = open(csv_path)
        csvreader = csv.reader(file, delimiter=";")
        for row in csvreader:
            self.data.append(row)
        self.data.remove(self.data[0])  # Removes header row
        for row in self.data:
            temp = row[0].split(".")
            row[0] = datetime.strptime(temp[0], '%Y-%m-%dT%H:%M:%S')
        print(self.data)
        print("Raw sensor data saved to memory.\n")

    def getSensorData(self, sensor, timestamp):
        result = []
        for row in self.data:
            if row[1] == sensor and row[0] < timestamp:
                result.append(row)
        return result


if __name__ == "__main__":
    dataRepo = DataRepository("test_data.csv")
    timestamp_input = datetime(
        year=2017, month=2, day=5, hour=13, minute=14, second=31)
    res = dataRepo.getSensorData("Sensor4", timestamp_input)
    print(res)
