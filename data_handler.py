import datetime

from data_repo import DataRepository
from pollutant_value import PollutantValue
import csv
import math
import numpy
import traceback


def distance(coord_1, coord_2):
    lat_1, long_1 = coord_1
    lat_2, long_2 = coord_2
    return 12742 * math.asin(math.sqrt(
        math.sin((math.radians(lat_2) - math.radians(lat_1)) / 2) ** 2 + math.cos(math.radians(lat_1)) * math.cos(
            math.radians(lat_2)) * math.sin((math.radians(long_2) - math.radians(long_1)) / 2) ** 2))


def calculate_aqi(concentration, intervals):
    aqi_low, aqi_high = intervals[1]
    bp_low, bp_high = intervals[0]
    return ((aqi_high - aqi_low) / (bp_high - bp_low)) * (concentration - bp_low) + aqi_low


def find_bound(average, bounds):
    interval = ((-28, -1), (-28, -1))
    for bound in bounds:
        aqi_low, aqi_high = bound[0]
        if aqi_low <= average <= aqi_high:
            interval = bound
    return interval


# AQI Calculation Values
o3_8hrbounds = [((0.0, 0.054), (0, 50)), ((0.055, 0.070), (51, 100)), ((0.071, 0.085), (101, 150)),
                ((0.086, 0.105), (151, 200)), ((0.106, 0.200), (201, 250))]
o3_1hrbounds = [((0.125, 0.164), (101, 150)), ((0.165, 0.204), (151, 200)),
                ((0.205, 0.404), (201, 300)), ((0.405, 0.504), (301, 400)), ((0.505, 0.604), (401, 500))]
pm10_bounds = [((0, 54), (0, 50)), ((55, 154), (51, 100)), ((155, 254), (101, 150)),
               ((255, 354), (151, 200)), ((355, 424), (201, 300)), ((425, 504), (301, 400)), ((505, 604), (401, 500))]
so2_1hrbounds = [((0, 35), (0, 50)), ((36, 75), (51, 100)), ((76, 185), (101, 150)), ((186, 304), (151, 200))]
so2_24hrbounds = [((305, 604), (201, 300)), ((605, 804), (301, 400)), ((805, 1004), (401, 500))]
no2_bounds = [((0, 53), (0, 50)), ((54, 100), (51, 100)), ((101, 360), (101, 150)),
              ((361, 649), (151, 200)), ((650, 1249), (201, 300)), ((1250, 1649), (301, 400)),
              ((1650, 2049), (401, 500))]


class DataHandler:

    def __init__(self, csv_path):
        self.data_repo = DataRepository(csv_path)
        self.sensor_coordinates = []
        self.max_distance = 1000
        with open('Sensors.csv') as sensor_file:
            sensor_csv = csv.DictReader(sensor_file, delimiter=';')
            for sid in sensor_csv:
                self.sensor_coordinates.append((sid["SensorID"], (float(sid["Latitude"]), float(sid["Longitude"]))))

    def get_air_quality_timespan(self, coord, time_stamp_start, time_stamp_end):
        used_timestamps = []
        total_air_qualities = []
        no2_air_qualities = []
        so2_air_qualities = []
        pm10_air_qualities = []
        o3_air_qualities = []
        sensor_error_count = 0
        timespan_error_count = 0
        for value in self.data_repo.data:
            if time_stamp_start <= value[0] <= time_stamp_end:
                used_timestamps.append(value[0])
        for timestamp in used_timestamps:
            result = self.get_air_quality(coord, timestamp)
            if result[0] != -1 and result[0] != -2:
                total_air_qualities.append(result[0])
                no2_air_qualities.append(result[1][0])
                so2_air_qualities.append(result[1][1])
                pm10_air_qualities.append(result[1][2])
                o3_air_qualities.append(result[1][3])
        if len(total_air_qualities) == 0:
            if self.get_air_quality(coord, time_stamp_start)[0] == -1:
                return -1, [0, 0, 0, 0]
            else:
                return -2, [0, 0, 0, 0]
        else:
            return numpy.mean(total_air_qualities), [numpy.mean(no2_air_qualities), numpy.mean(so2_air_qualities),
                                                     numpy.mean(pm10_air_qualities), numpy.mean(o3_air_qualities)]

    def get_air_quality(self, coord, time_stamp):
        air_quality_list = []
        sensors_used = []
        data = []
        for coord2 in self.sensor_coordinates:
            if distance(coord, coord2[1]) <= self.max_distance:
                sensors_used.append(coord2[0])
        if len(sensors_used) == 0:
            return -1, air_quality_list
        for i in sensors_used:
            for j in self.data_repo.getSensorData(i, time_stamp):
                data.append(j)
        if len(data) == 0:
            # -2 is error code for no valid data within given time constraints
            return -2, air_quality_list
        for i in range(0, 4):
            air_quality_list.append(self.calculate_mean_air_quality(i, time_stamp, data))

        total_air_quality = max(air_quality_list)

        return total_air_quality, air_quality_list

    def calculate_mean_air_quality(self, pollutant, timestamp, data):
        result = -27
        try:
            if pollutant == 0:
                relevant_values = []
                for entry in data:
                    if entry.type == 0 and (timestamp - entry.timestamp).total_seconds() <= 3600:
                        relevant_values.append(entry.value)
                # used conversion factors assume 25 degrees celcius and 1 atm pressure
                average = 1.88 * numpy.mean(relevant_values)
                interval = find_bound(average, no2_bounds)
                result = calculate_aqi(average, interval)
            elif pollutant == 1:
                relevant_values = []
                relevant_values24 = []
                for entry in data:
                    if entry.type == 1:
                        if (timestamp - entry.timestamp).total_seconds() <= 3600:
                            relevant_values.append(entry.value)
                        if (timestamp - entry.timestamp).total_seconds() <= 86400:
                            relevant_values24.append(entry.value)
                average = 2.62 * numpy.mean(relevant_values)
                average24 = 2.62 * numpy.mean(relevant_values24)
                # the following emulates the decision tree of which values to use as outlined by the US EPA
                if average < 305:
                    interval = find_bound(average, so2_1hrbounds)
                    result = calculate_aqi(average, interval)
                elif average24 < 305:
                    result = calculate_aqi(average, ((303, 304), (200, 200)))
                else:
                    interval = find_bound(average24, so2_24hrbounds)
                    result = calculate_aqi(average24, interval)
            elif pollutant == 2:
                relevant_values = []
                for entry in data:
                    if entry.type == 2 and (timestamp - entry.timestamp).total_seconds() <= 86400:
                        relevant_values.append(entry.value)
                # required units already match data, so no conversion factor
                average = numpy.mean(relevant_values)
                interval = find_bound(average, pm10_bounds)
                result = calculate_aqi(average, interval)
            elif pollutant == 3:
                relevant_values = []
                relevant_values8 = []
                for entry in data:
                    if entry.type == 3:
                        if (timestamp - entry.timestamp).total_seconds() <= 3600:
                            relevant_values.append(entry.value)
                        if (timestamp - entry.timestamp).total_seconds() <= 28800:
                            relevant_values8.append(entry.value)
                average = numpy.mean(relevant_values) if numpy.mean(relevant_values) >= 0.125 else 0.0
                average8 = numpy.mean(relevant_values8) if numpy.mean(relevant_values8) <= 0.200 else 0.0
                interval = find_bound(average, o3_1hrbounds)
                interval8 = find_bound(average8, o3_8hrbounds)
                results = [calculate_aqi(average, interval), calculate_aqi(average8, interval8)]
                result = max(results)
        except:
            traceback.print_exc()
        if result != -27:
            return result
        else:
            return "ERROR"
