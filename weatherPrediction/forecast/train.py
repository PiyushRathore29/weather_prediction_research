import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import pickle

# Load historical data
data = pd.read_csv('weather.csv')
data = data.dropna().drop_duplicates()

# Label encode categorical values
le = LabelEncoder()
data['WindGustDir'] = le.fit_transform(data['WindGustDir'])
data['RainTomorrow'] = le.fit_transform(data['RainTomorrow'])

# Train Rain Prediction Model
X = data[['MinTemp', 'MaxTemp', 'WindGustDir', 'WindGustSpeed', 'Humidity', 'Pressure', 'Temp']]
y = data['RainTomorrow']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rain_model = RandomForestClassifier(n_estimators=100, random_state=42)
rain_model.fit(X_train, y_train)

# Train Regression Models
def prepare_regression_data(data, feature):
    X = data[feature].iloc[:-1].values.reshape(-1, 1)
    y = data[feature].iloc[1:].values
    return X, y

X_temp, y_temp = prepare_regression_data(data, 'Temp')
X_hum, y_hum = prepare_regression_data(data, 'Humidity')

temp_model = RandomForestRegressor(n_estimators=100, random_state=42)
temp_model.fit(X_temp, y_temp)

hum_model = RandomForestRegressor(n_estimators=100, random_state=42)
hum_model.fit(X_hum, y_hum)

# Save Models
with open('rain_model.pkl', 'wb') as f:
    pickle.dump(rain_model, f)

with open('temp_model.pkl', 'wb') as f:
    pickle.dump(temp_model, f)

with open('hum_model.pkl', 'wb') as f:
    pickle.dump(hum_model, f)

with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)

print("Models saved successfully!")

