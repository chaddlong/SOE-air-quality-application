import unittest
from datetime import datetime
from data_repo import DataRepository

class TestSensorData(unittest.TestCase):
    
    def test_getSensorData(self):
        data_repo = DataRepository("test_data.csv")
        
        result = data_repo.getSensorData( "Sensor4", datetime(
        year=2017, month=2, day=5, hour=13, minute=14, second=31))[0][3]
        
        self.assertEqual(result, '15.9811820824628' )
        print("Does it work?")

if __name__ == '__main__':
    unittest.main()

#class TestDataHandler(unittest.TestCase):

   # def test_
