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


def calculate_mean_air_quality(pollutant, timestamp, data):
    # Placeholder value to initialize the result variable for later usage
    result = -27
    try:
        # When pollutant is NO2
        if pollutant == 0:
            relevant_values = []
            for entry in data:
                # Data from the past hour is used for 1-hour average
                if entry.type == 0 and (timestamp - entry.timestamp).total_seconds() <= 3600:
                    relevant_values.append(entry.value)
            # used conversion factors assume 25 degrees celcius and 1 atm pressure
            average = 1.88 * numpy.mean(relevant_values)
            interval = find_bound(average, no2_bounds)
            result = calculate_aqi(average, interval)
        # When pollutant is SO2
        elif pollutant == 1:
            relevant_values = []
            relevant_values24 = []
            for entry in data:
                if entry.type == 1:
                    # Gets data values for 1-hour and 8-hour averages
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
        # When pollutant is PM10
        elif pollutant == 2:
            relevant_values = []
            for entry in data:
                if entry.type == 2 and (timestamp - entry.timestamp).total_seconds() <= 86400:
                    relevant_values.append(entry.value)
            # required units already match data, so no conversion factor
            average = numpy.mean(relevant_values)
            interval = find_bound(average, pm10_bounds)
            result = calculate_aqi(average, interval)
        # When pollutant is O3
        elif pollutant == 3:
            relevant_values = []
            relevant_values8 = []
            for entry in data:
                if entry.type == 3:
                    if (timestamp - entry.timestamp).total_seconds() <= 3600:
                        relevant_values.append(entry.value)
                    if (timestamp - entry.timestamp).total_seconds() <= 28800:
                        relevant_values8.append(entry.value)
            average = numpy.mean(relevant_values) if numpy.mean(
                relevant_values) >= 0.125 else 0.0
            average8 = numpy.mean(relevant_values8) if numpy.mean(
                relevant_values8) <= 0.200 else 0.0
            interval = find_bound(average, o3_1hrbounds)
            interval8 = find_bound(average8, o3_8hrbounds)
            # Both 1-hour and 8-hour averages are found, the larger of the two being used
            results = [calculate_aqi(average, interval),
                       calculate_aqi(average8, interval8)]
            result = max(results)
    except:
        traceback.print_exc()
    # If the calculation worked, this should not be -27
    if result != -27:
        return result
    else:
        return "ERROR"


# AQI Calculation Values
# Each tuple contains two tuples, the first containing the range of the pollutant value in its respective unit
# (conversion is done later on), and the second containing the respective AQI values. Some bounds use averages
# from multiple timeframes depending on the value. For instance, some ranges require a 1-hour average while
# other ranges require an 8-hour average.
o3_8hrbounds = [((0.0, 0.054), (0, 50)), ((0.055, 0.070), (51, 100)), ((0.071, 0.085), (101, 150)),
                ((0.086, 0.105), (151, 200)), ((0.106, 0.200), (201, 250))]
o3_1hrbounds = [((0.125, 0.164), (101, 150)), ((0.165, 0.204), (151, 200)),
                ((0.205, 0.404), (201, 300)), ((0.405, 0.504), (301, 400)), ((0.505, 0.604), (401, 500))]
pm10_bounds = [((0, 54), (0, 50)), ((55, 154), (51, 100)), ((155, 254), (101, 150)),
               ((255, 354), (151, 200)), ((355, 424), (201, 300)), ((425, 504), (301, 400)), ((505, 604), (401, 500))]
so2_1hrbounds = [((0, 35), (0, 50)), ((36, 75), (51, 100)),
                 ((76, 185), (101, 150)), ((186, 304), (151, 200))]
so2_24hrbounds = [((305, 604), (201, 300)), ((605, 804),
                                             (301, 400)), ((805, 1004), (401, 500))]
no2_bounds = [((0, 53), (0, 50)), ((54, 100), (51, 100)), ((101, 360), (101, 150)),
              ((361, 649), (151, 200)), ((650, 1249),
                                         (201, 300)), ((1250, 1649), (301, 400)),
              ((1650, 2049), (401, 500))]


class DataHandler:

    def __init__(self, csv_path):
        self.data_repo = DataRepository(csv_path)
        self.sensor_coordinates = []
        self.max_distance = 1000
        with open('Sensors.csv') as sensor_file:
            sensor_csv = csv.DictReader(sensor_file, delimiter=';')
            for sid in sensor_csv:
                self.sensor_coordinates.append(
                    (sid["SensorID"], (float(sid["Latitude"]), float(sid["Longitude"]))))

    def get_air_quality_timespan(self, coord, time_stamp_start, time_stamp_end):
        # Creates an array to keep track of which timestamps are used to gather data from
        used_timestamps = []
        # Creates arrays to hold the relevant values at each checked timestamp, which are averaged later
        total_air_qualities = []
        no2_air_qualities = []
        so2_air_qualities = []
        pm10_air_qualities = []
        o3_air_qualities = []
        # Only uses data points whose timestamps fall within the specified range
        for value in self.data_repo.data:
            if time_stamp_start <= value[0] <= time_stamp_end:
                used_timestamps.append(value[0])
        for timestamp in used_timestamps:
            result = self.get_air_quality(coord, timestamp)
            # Makes sure there are no errors with individual air qualities to prevent array access errors
            if result[0] != -1 and result[0] != -2:
                total_air_qualities.append(result[0])
                no2_air_qualities.append(result[1][0])
                so2_air_qualities.append(result[1][1])
                pm10_air_qualities.append(result[1][2])
                o3_air_qualities.append(result[1][3])
        # This indicates that something went horribly wrong
        if len(total_air_qualities) == 0:
            # Sensor location doesn't change, so if a single air quality
            # returns a no-sensor error, the same is true for all air qualities at the given coordinates,
            # regardless of timespan
            if self.get_air_quality(coord, time_stamp_start)[0] == -1:
                return -1, [0, 0, 0, 0]
            else:
                # If there are sensors within range, the error must be a lack of data in the timespan
                return -2, [0, 0, 0, 0]
        else:
            return numpy.mean(total_air_qualities), [numpy.mean(no2_air_qualities), numpy.mean(so2_air_qualities),
                                                     numpy.mean(pm10_air_qualities), numpy.mean(o3_air_qualities)]

    def get_air_quality(self, coord, time_stamp):
        # Used to hold air qualities for each pollutant
        air_quality_list = []
        sensors_used = []
        # Holds PollutantValue instances for use
        data = []
        # Finds sensors within range
        for coord2 in self.sensor_coordinates:
            if distance(coord, coord2[1]) <= self.max_distance:
                sensors_used.append(coord2[0])
        # If there aren't sensors within range, return a no-sensor error
        if len(sensors_used) == 0:
            return -1, air_quality_list
        # Get data
        for i in sensors_used:
            for j in self.data_repo.getSensorData(i, time_stamp):
                data.append(j)
        if len(data) == 0:
            # -2 is error code for no valid data within given time constraints
            return -2, air_quality_list
        # Calculates the air quality for each pollutant
        for i in range(0, 4):
            air_quality_list.append(
                calculate_mean_air_quality(i, time_stamp, data))

        # Total air quality is the maximum pollutant air quality value
        total_air_quality = max(air_quality_list)

        return total_air_quality, air_quality_list

    def get_similar_sensors(self, time_stamp_start, time_stamp_end):
        sensor_values = {"Sensor0": [], "Sensor1": [], "Sensor2": [],
                         "Sensor3": [], "Sensor4": [], "Sensor5": [], "Sensor6": [], "Sensor7": [], "Sensor8": [], "Sensor9": []}
        for value in self.data_repo.data:
            if time_stamp_start <= value[0] <= time_stamp_end:
                # [datetime.datetime(2017, 1, 1, 3, 31, 22), 'Sensor5', 'PM10', '26.0549070206503', '']
                sensor_values[value[1]].append((value[0], value[2], value[3]))

        similar_sensors = {}
        print(sensor_values)
        for source_sensor, source_values in sensor_values:
            similar_sensors[source_sensor] = []
            for target_sensor, target_values in sensor_values:
                if source_sensor != target_sensor and source_values[2] == target_values[2]:
                    if abs(source_values[3]-target_values[3]) < 2:
                        similar_sensors[source_sensor].append(target_sensor)
        return similar_sensors
