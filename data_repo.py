import csv
from datetime import datetime
from pollutant_value import PollutantValue
import re


def switch(pollutant):
    if pollutant == "NO2":
        return 0
    elif pollutant == "SO2":
        return 1
    elif pollutant == "PM10":
        return 2
    elif pollutant == "O3":
        return 3


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
        print("Raw sensor data saved to memory.\n")

    def getSensorData(self, sensor, timestamp):
        result = []
        sensor = int(re.search('(?<=Sensor)[0-9]+', sensor)[0])
        for row in self.data:
            sensor_number = int(re.search('(?<=Sensor)[0-9]+', row[1])[0])
            if sensor_number == sensor and row[0] <= timestamp:
                result.append(PollutantValue(
                    float(row[3]), sensor_number, row[0], switch(row[2])))
        return result
