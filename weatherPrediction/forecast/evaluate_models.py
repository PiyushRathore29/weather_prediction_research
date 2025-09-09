import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import mean_squared_error, accuracy_score, r2_score
from sklearn.model_selection import train_test_split

# === Load historical data ===
data = pd.read_csv('weather.csv').dropna().drop_duplicates()

# === Load saved models ===
with open('rain_model.pkl', 'rb') as f:
    rain_model = pickle.load(f)

with open('temp_model.pkl', 'rb') as f:
    temp_model = pickle.load(f)

with open('hum_model.pkl', 'rb') as f:
    hum_model = pickle.load(f)

with open('label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)

# === Rain Prediction Model Evaluation ===
data['WindGustDir'] = le.transform(data['WindGustDir'])
data['RainTomorrow'] = le.transform(data['RainTomorrow'])

X_rain = data[['MinTemp', 'MaxTemp', 'WindGustDir', 'WindGustSpeed', 'Humidity', 'Pressure', 'Temp']]
y_rain = data['RainTomorrow']

X_train, X_test, y_train, y_test = train_test_split(X_rain, y_rain, test_size=0.2, random_state=42)
y_pred_rain = rain_model.predict(X_test)

rain_accuracy = accuracy_score(y_test, y_pred_rain)
rain_mse = mean_squared_error(y_test, y_pred_rain)

print("\n=== Rain Prediction Model ===")
print(f"Accuracy: {rain_accuracy * 100:.2f}%")
print(f"Mean Squared Error: {rain_mse:.4f}")

# === Regression Models Evaluation Function ===
def evaluate_regression(model, feature_name):
    X = data[feature_name].iloc[:-1].values.reshape(-1, 1)
    y_true = data[feature_name].iloc[1:].values
    y_pred = model.predict(X)

    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    print(f"\n=== {feature_name} Prediction Model ===")
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"R² Score: {r2:.4f}")

# Evaluate Temperature & Humidity Models
evaluate_regression(temp_model, 'Temp')
evaluate_regression(hum_model, 'Humidity')
