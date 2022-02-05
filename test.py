import unittest
from ForecastData import Get_Realized_Data
from datetime import datetime, timedelta

class TestGetRealizedData(unittest.TestCase):
    def test_get_data(self):
        """
        Test that it retrieves the most recent tuple.
        :return:
        """
        now = datetime.now()
        now_input = now
        now = now + timedelta(hours=6)
        while now.minute not in [00,15,30,45]:
            now = now - timedelta(minutes=1)
        now = now.strftime("%H")
        real_time = Get_Realized_Data(now_input).hours_list()[-1]
        self.assertEqual(real_time, now)

if __name__ == '__main__':
    unittest.main()