# Weather Prediction System using Random Forest and Django

## 🔑 Key Components of the Project

### 1. Dataset

- Real-world weather dataset (mention its source, e.g., Kaggle, NOAA,
  IMD, or any other).
- Features used: temperature, humidity, wind speed, pressure,
  precipitation, etc.

### 2. Data Preprocessing

- Cleaning (handling missing values, outliers).
- Feature selection (keeping only relevant features).
- Normalization or scaling if required.

### 3. Model: Random Forest Classifier/Regressor

- Trained on weather features.
- Predicts weather condition (sunny, rainy, cloudy, etc.) or numeric
  values (like temperature).
- Performance metrics: accuracy, RMSE, confusion matrix, etc.

### 4. Backend: Django

- API integration: Model is served through Django views/REST API.
- User can input weather parameters through a web form.
- Prediction result is shown dynamically.

### 5. Frontend (if implemented)

- HTML/CSS/Bootstrap for UI.
- Prediction output displayed neatly.

### 6. Deployment (Optional)

- Hosted on local server or cloud (Heroku, AWS, PythonAnywhere).

---

## 🌟 Features

- Real-time prediction of weather.
- Interactive web interface using Django.
- Robust machine learning model (Random Forest).
- Handles real-world dataset.
- Extendable for future improvements (adding more ML/DL models).

---

## 📊 Challenges Faced

- Data quality issues (missing, noisy values).
- Model overfitting/underfitting.
- Balancing performance vs interpretability.
- Deployment difficulties (connecting ML model with Django).

## Training and Building Dataset Files

### Install dependencies

- pip install packaging

### Run training and evaluation scripts

#### Train the models

- python -u "C:\Users\ratho\Desktop\weather prediction system\weatherPrediction\forecast\train.py"

#### Evaluate the models

- python -u "C:\Users\ratho\Desktop\weather prediction system\weatherPrediction\forecast\evaluate_models.py"

#### Generate views and additional processed files

- python -u "C:\Users\ratho\Desktop\weather prediction system\weatherPrediction\forecast\views.py"

## Steps to Start App

### 1. Activate virtual environment

.\venv\Scripts\activate # On Windows

### OR

- source venv/bin/activate # On macOS/Linux

### 2. Navigate to your Django project folder

- cd project_name

### 3. Run the Django development server

- python manage.py runserver
