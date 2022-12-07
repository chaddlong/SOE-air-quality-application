from data_repo import DataRepository
from pollutant_value import PollutantValue
import csv
import math


def distance(coord_1, coord_2):
    lat_1, long_1 = coord_1
    lat_2, long_2 = coord_2
    return 12742 * math.asin(math.sqrt(
        math.sin((math.radians(lat_2) - math.radians(lat_1)) / 2) ** 2 + math.cos(math.radians(lat_1)) * math.cos(
            math.radians(lat_2)) * math.sin((math.radians(long_2) - math.radians(long_1)) / 2) ** 2))


#AQI Calculation Values
o3_8hrbounds = [((0.0, 0.054), (0, 50)), ((0.055, 0.070), (51, 100)), ((0.071, 0.085), (101, 150)),
                ((0.086, 0.105), (151, 200)), ((0.106, 0.200), (201, 250))]
o3_1hrbounds = [((0.125, 0.164), (101, 150)), ((0.165, 0.204), (151, 200)),
                ((0.205, 0.404), (201, 300)), ((0.405, 0.504), (301, 400)), ((0.505, 0.604), (401, 500))]
pm10_bounds = [((0, 54), (0, 50)), ((55, 154), (51, 100)), ((155, 254), (101, 150)),
               ((255, 354), (151, 200)), ((355, 424), (201, 300)), ((425, 504), (301, 400)), ((505, 604), (401, 500))]
so2_1hrbounds = [((0, 35), (0, 50)), ((36, 75), (51, 100)), ((76, 185), (101, 150)), ((186, 304), (151, 200))]
so2_24hrbounds = [((305, 604), (201, 300)), ((605, 804), (301, 400)), ((805, 1004), (401, 500))]
no2_bounds = [((0, 53), (0, 50)), ((54, 100), (51, 100)), ((101, 360), (101, 150)),
              ((361, 649), (151, 200)), ((650, 1249), (201, 300)), ((1250, 1649), (301, 400)), ((1650, 2049), (401, 500))]


class DataHandler:

    def __init__(self, csv_path):
        self.data_repo = DataRepository(csv_path)
        self.sensor_coordinates = []
        self.max_distance = 1000
        with open('Sensors.csv') as sensor_file:
            sensor_csv = csv.DictReader(sensor_file)
            for sid in sensor_csv:
                self.sensor_coordinates.append((0, (sid[1], sid[2])))

    def get_air_quality(self, coord, time_stamp):
        lat, long = coord
        air_quality_list = []
        for i in range(0, 3):
            air_quality_list.append(self.calculate_mean_air_quality(i, time_stamp, (lat, long)))

        total_air_quality = max(air_quality_list)

        return total_air_quality, air_quality_list

    def calculate_mean_air_quality(self, pollutant, timestamp, coord):
        sensors_used = []
        data = []
        for coord2 in self.sensor_coordinates:
            if distance(coord, coord2[1]) <= self.max_distance:
                sensors_used.append(coord2[0])
        for i in sensors_used:
            data.append(self.data_repo.getSensorData(i, timestamp))

        if pollutant == 0:
            testing = "0"

