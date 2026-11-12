from flask import Flask, request, render_template
import pickle
import numpy as np
import time
import pandas as pd

app = Flask(__name__)

weather_classes = ['clear', 'cloudy', 'drizzly', 'foggy', 'hazey', 'misty', 'rainy', 'smokey', 'thunderstorm']

def load_model(model_path='model/model.pkl'):
    # W01 fix: Close the model file automatically after loading.
    with open(model_path, 'rb') as model_file:
        return pickle.load(model_file)

def classify_weather(features):
	model = load_model()
	start = time.time()
	#QA 02 Warning: The model was trained with named colums but this input is a numpy array without column names. producing a user warning.
	#check the expected features names and order before changing the input.

	#W02 fix: Label the inputs with the model's training column names.
	# The values must stay in the same order as these columns.

	named_features = pd.DataFrame(features, columns=[
    'temp', 'pressure', 'humidity', 'wind_speed', 'wind_deg',
    'rain_1h', 'rain_3h', 'snow_3h', 'clouds_all'])
	
	prediction_index = model.predict(named_features)[0]

	latency = round((time.time() - start) * 1000, 2) #we are here
	#QA 01 defect fix : use the models predicted index to select the weather label 
	prediction = weather_classes[prediction_index]
	
	return prediction, latency


@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		try:
			# QA 02 defect fix: Covert required form values to floats so the modul receives numbers.
			temperature = float(request.form['temperature'])
			pressure = float(request.form['pressure'])
			humidity = float(request.form['humidity'])
			wind_speed = float(request.form['wind_speed'])
			wind_deg = float(request.form['wind_deg'])
			rain_1h = float(request.form.get('rain_1h', 0) or 0)
			rain_3h = float(request.form.get('rain_3h', 0) or 0)
			snow = float(request.form.get('snow', 0) or 0)
			clouds = float(request.form.get('clouds', 0) or 0)

			features = np.array([
				temperature, pressure, humidity,
				wind_speed, wind_deg, rain_1h,
				rain_3h, snow, clouds
			]).reshape(1, -1)

			
			prediction, latency = classify_weather(features)


			return render_template('result.html', prediction=prediction, latency=latency)

		except Exception as e:
			error_msg = f"Error processing input: {e}"
			return render_template('form.html', error=error_msg)
	# GET method: show the input form
	return render_template('form.html')


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)
