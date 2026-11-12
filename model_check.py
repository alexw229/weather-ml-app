import pandas as pd
from app import load_model, weather_classes

model = load_model()

features = pd.DataFrame(
    [[289.47, 1015, 88, 2, 300, 0, 0, 0, 20]],
    columns=[
        'temp', 'pressure', 'humidity', 'wind_speed', 'wind_deg',
        'rain_1h', 'rain_3h', 'snow_3h', 'clouds_all'
    ]
)

prediction_index = model.predict(features)[0]
probabilities = model.predict_proba(features)[0]

print("Model classes:", model.classes_)
print("Predicted index:", prediction_index)
print("Mapped weather label:", weather_classes[prediction_index])
print("Starter test expects: foggy")
print()
print("Model confidence for each class:")
for label, p in zip(weather_classes, probabilities):
    print(f"  {label}: {p:.1%}")