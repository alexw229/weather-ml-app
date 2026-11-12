import unittest
import numpy as np
from app import app, classify_weather, load_model


class TestUnit(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_post_missing_field(self):
        # Leave out wind_speed to check missing input handling.
        form_data = {
            'temperature': '270.277',
            'pressure': '1006',
            'humidity': '84',
            'wind_deg': '274',
            'rain_1h': '0',
            'rain_3h': '0',
            'snow': '0',
            'clouds': '9'
        }

        response = self.client.post('/', data=form_data)
        html = response.data.decode('utf-8')

        self.assertIn(
            'Error processing input:',
            html,
            'Missing input should display an error message.'
        )
        self.assertNotIn(
            'The weather is:',
            html,
            'Missing input should not produce a prediction.'
        )

    def test_model_can_be_loaded(self):
        # Check that the saved model loads and can make predictions.
        model = load_model()

        self.assertIsNotNone(model, 'The model should not be None.')
        self.assertTrue(
            callable(getattr(model, 'predict', None)),
            'The loaded model should have a predict method.'
        )

    def test_clear_classification_output(self):
        # Use the clear-weather example supplied in the starter file.
        test_input = np.array([
            269.686, 1002, 78, 0, 23, 0, 0, 0, 0
        ]).reshape(1, -1)

        class_result, _ = classify_weather(test_input)

        self.assertEqual(
            class_result,
            'clear',
            'The supplied clear example should return clear.'
        )

    def test_rainy_classification_output(self):
        # Use the rainy-weather example supplied in the starter file.
        test_input = np.array([
            279.626, 998, 99, 1, 314, 0.3, 0, 0, 88
        ]).reshape(1, -1)

        class_result, _ = classify_weather(test_input)

        self.assertEqual(
            class_result,
            'rainy',
            'The supplied rainy example should return rainy.'
        )

    def test_foggy_classification_output(self):
        #QA 03 Defect: The started instructions expect foggy for this input.
        #A seperate check of the suplied model returns index 1 (cloudy).
        #confirm the test input and class mapping before changing the expected result.
        
        # Keep the expected result specified in the starter file.
        test_input = np.array([
            289.47, 1015, 88, 2, 300, 0, 0, 0, 20
        ]).reshape(1, -1)

        class_result, _ = classify_weather(test_input)

        self.assertEqual(
            class_result,
            'foggy',
            'The supplied foggy example should return foggy.'
        )


if __name__ == '__main__':
    unittest.main()