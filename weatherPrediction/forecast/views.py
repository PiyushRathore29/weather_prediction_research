from django.shortcuts import render
import requests
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime, timedelta
import pytz

# --- API CONFIG ---
API_KEY = '24338b771f38ec831245579deed29861'
BASE_URL = 'https://api.openweathermap.org/data/2.5/'

# --- MODEL PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')

def load_model(filename):
    with open(os.path.join(MODEL_DIR, filename), 'rb') as f:
        return pickle.load(f)

# Load all models once
rain_model = load_model('rain_model.pkl')
temp_model = load_model('temp_model.pkl')
hum_model = load_model('hum_model.pkl')
label_encoder = load_model('label_encoder.pkl')

# --- GET WEATHER DATA ---
def get_current_weather(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return {
        'city': data['name'],
        'current_temp': round(data['main']['temp']),
        'feels_like': round(data['main']['feels_like']),
        'temp_min': round(data['main']['temp_min']),
        'temp_max': round(data['main']['temp_max']),
        'humidity': round(data['main']['humidity']),
        'description': data['weather'][0]['description'],
        'country': data['sys']['country'],
        'wind_gust_dir': data['wind']['deg'],
        'pressure': data['main']['pressure'],
        'wind_gust_speed': data['wind']['speed'],
        'clouds': data['clouds']['all'],
        'visibility': data['visibility'],
    }

# --- PREDICT FUTURE VALUES ---
def predict_future(model, current_value):
    predictions = [current_value]
    for _ in range(5):
        next_val = model.predict(np.array([[predictions[-1]]]))
        predictions.append(next_val[0])
    return predictions[1:]

# --- MAIN VIEW ---
def weather_view(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        current_weather = get_current_weather(city)

        # Convert wind degrees to compass direction
        wind_deg = current_weather['wind_gust_dir'] % 360
        compass_points = [
            ("N", 0, 11.25), ("NNE", 11.25, 33.75), ("NE", 33.75, 56.25),
            ("ENE", 56.25, 78.75), ("E", 78.75, 101.25), ("ESE", 101.25, 123.75),
            ("SE", 123.75, 146.25), ("SSE", 146.25, 168.75), ("S", 168.75, 191.25),
            ("SSW", 191.25, 213.75), ("SW", 213.75, 236.25), ("WSW", 236.25, 258.75),
            ("W", 258.75, 281.25), ("WNW", 281.25, 303.75), ("NW", 303.75, 326.25),
            ("NNW", 326.25, 348.75), ("N", 348.75, 360)
        ]
        compass_direction = next((point for point, start, end in compass_points if start <= wind_deg < end), "N")
        compass_encoded = label_encoder.transform([compass_direction])[0] if compass_direction in label_encoder.classes_ else -1

        # Format current weather for prediction
        current_input = pd.DataFrame([{
            'MinTemp': current_weather['temp_min'],
            'MaxTemp': current_weather['temp_max'],
            'WindGustDir': compass_encoded,
            'WindGustSpeed': current_weather['wind_gust_speed'],
            'Humidity': current_weather['humidity'],
            'Pressure': current_weather['pressure'],
            'Temp': current_weather['current_temp'],
        }])

        rain_prediction = rain_model.predict(current_input)[0]
        future_temp = predict_future(temp_model, current_weather['temp_min'])
        future_hum = predict_future(hum_model, current_weather['humidity'])

        # Future Dates (next 5 days)
        timezone = pytz.timezone('Asia/Kolkata')
        now = datetime.now(timezone)
        next_day = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        future_days = [(next_day + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]

        # Context for Template
        context = {
            'location': city,
            'current_temp': current_weather['current_temp'],
            'MinTemp': current_weather['temp_min'],
            'MaxTemp': current_weather['temp_max'],
            'feels_like': current_weather['feels_like'],
            'humidity': current_weather['humidity'],
            'clouds': current_weather['clouds'],
            'description': current_weather['description'],
            'city': current_weather['city'],
            'country': current_weather['country'],
            'time': now,
            'date': now.strftime("%B %d, %Y"),
            'wind': current_weather['wind_gust_speed'],
            'pressure': current_weather['pressure'],
            'visibility': current_weather['visibility'],
            'time1': future_days[0], 'time2': future_days[1], 'time3': future_days[2],
            'time4': future_days[3], 'time5': future_days[4],
            'temp1': round(future_temp[0], 1), 'temp2': round(future_temp[1], 1),
            'temp3': round(future_temp[2], 1), 'temp4': round(future_temp[3], 1),
            'temp5': round(future_temp[4], 1),
            'hum1': round(future_hum[0], 1), 'hum2': round(future_hum[1], 1),
            'hum3': round(future_hum[2], 1), 'hum4': round(future_hum[3], 1),
            'hum5': round(future_hum[4], 1),
            'rain_prediction': 'Yes' if rain_prediction == 1 else 'No',
        }
        return render(request, 'weather.html', context)

    return render(request, 'weather.html')

def index_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')
