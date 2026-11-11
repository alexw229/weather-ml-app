import unittest
from app import app


class TestAppSmoke(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_prediction_route_success(self):
        # Check that the home page responds successfully.
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

    def test_get_form(self):
        # Check that the page contains the weather input form.
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        self.assertIn('<form', html)
        self.assertIn('name="temperature"', html)
        self.assertIn('name="pressure"', html)
        self.assertIn('name="humidity"', html)
        self.assertIn('name="wind_speed"', html)
        self.assertIn('name="wind_deg"', html)
        self.assertIn('name="rain_1h"', html)
        self.assertIn('name="rain_3h"', html)
        self.assertIn('name="snow"', html)
        self.assertIn('name="clouds"', html)
        self.assertIn('Predict', html)


if __name__ == '__main__':
    unittest.main()