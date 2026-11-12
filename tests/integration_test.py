import unittest
from app import app


class TestModelAppIntegration(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_model_app_integration(self):
        # Use the valid input supplied in the starter file.
        form_data = {
            'temperature': '275.15',  # Kelvin
            'pressure': '1013',       # hPa
            'humidity': '85',         # %
            'wind_speed': '3.6',      # m/s
            'wind_deg': '180',        # degrees
            'rain_1h': '0',
            'rain_3h': '0',
            'snow': '0',
            'clouds': '20'
        }

        response = self.client.post('/', data=form_data)
        html = response.data.decode('utf-8')

        self.assertEqual(response.status_code, 200)

        self.assertNotIn(
            'Error processing input:',
            html,
            'Valid input should not display an error.'
        )

        self.assertIn(
            'The weather is:',
            html,
            'The result page should display a weather prediction.'
        )

        self.assertIn(
            'Prediction time:',
            html,
            'The result page should display the prediction time.'
        )

        valid_classes = [
            'clear', 'cloudy', 'drizzly', 'foggy', 'hazey',
            'misty', 'rainy', 'smokey', 'thunderstorm'
        ]

        html_text = html.lower()
        found = any(weather in html_text for weather in valid_classes)

        self.assertTrue(
            found,
            'The prediction should contain a recognised weather class.'
        )

        self.assertRegex(
            html,
            r'Prediction time:</strong>\s*\d+(?:\.\d+)?\s*ms',
            'Prediction time should be a non-negative number in milliseconds.'
        )


if __name__ == '__main__':
    unittest.main()