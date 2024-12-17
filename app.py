from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

app = Flask(__name__)

# Prometheus Metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['endpoint', 'method', 'status_code'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['endpoint'])

# Define Prometheus gauges for predicted AQI values
PREDICTED_AQI_LSTM = Gauge('predicted_aqi_lstm', 'Predicted AQI from LSTM model')
PREDICTED_AQI_ARIMA = Gauge('predicted_aqi_arima', 'Predicted AQI from ARIMA model')

# Load the LSTM model
lstm_model = tf.keras.models.load_model("pollution_trend_lstm.keras")

# Load the ARIMA model from the pickle file
with open('pollution_trend_arima_2_1_1.pkl', 'rb') as f:
    arima_model = pickle.load(f)

# Define feature names including all features used during training
FEATURES = [
    "temperature", "humidity", "weather", "hour", "day", "month",
    "co", "no2", "o3", "pm2_5", "pm10", "PRCP", "TAVG", "TMAX", "TMIN"
]
TARGET = "aqi_us"

# Load the training data to recreate scalers
data = pd.read_csv("final_data.csv")

# Recreate scalers and fit them
scaler = MinMaxScaler()
target_scaler = MinMaxScaler()
scaler.fit(data[FEATURES])  # Fit the feature scaler
target_scaler.fit(data[[TARGET]])  # Fit the target scaler

# Function to preprocess input for LSTM model
def preprocess_input(data):
    df = pd.DataFrame([data], columns=FEATURES)
    scaled_data = scaler.transform(df)
    repeated_data = np.tile(scaled_data, (5, 1))  # 5 time steps, same features
    return np.expand_dims(repeated_data, axis=0)  # Shape should be (1, 5, 15)

# Function to get ARIMA prediction
def arima_predict(data):
    df = pd.DataFrame([data], columns=FEATURES)
    scaled_data = scaler.transform(df)
    aqi_scaled = scaled_data[:, -1]  # Extracting the AQI feature
    prediction = arima_model.forecast(steps=1, exog=aqi_scaled.reshape(-1, 1))
    return prediction[0]

@app.route('/predict', methods=['POST'])
def predict():
    with REQUEST_LATENCY.labels(endpoint='/predict').time():
        try:
            input_data = request.json
            missing_features = [f for f in FEATURES if f not in input_data]
            if missing_features:
                REQUEST_COUNT.labels(endpoint='/predict', method='POST', status_code='400').inc()
                return jsonify({"error": f"Missing features: {missing_features}"}), 400

            feature_values = [input_data[f] for f in FEATURES]
            preprocessed_data = preprocess_input(feature_values)

            lstm_prediction = lstm_model.predict(preprocessed_data)
            arima_prediction = arima_predict(feature_values)

            predicted_aqi_lstm = float(target_scaler.inverse_transform(lstm_prediction.reshape(-1, 1))[0][0])
            predicted_aqi_arima = float(target_scaler.inverse_transform(arima_prediction.reshape(-1, 1))[0][0])

            # Set the predicted AQI values to Prometheus gauges
            PREDICTED_AQI_LSTM.set(predicted_aqi_lstm)
            PREDICTED_AQI_ARIMA.set(predicted_aqi_arima)

            REQUEST_COUNT.labels(endpoint='/predict', method='POST', status_code='200').inc()

            return jsonify({
                "predicted_aqi_lstm": predicted_aqi_lstm,
                "predicted_aqi_arima": predicted_aqi_arima
            })

        except Exception as e:
            print("Error during prediction:", str(e))
            REQUEST_COUNT.labels(endpoint='/predict', method='POST', status_code='500').inc()
            return jsonify({"error": "Internal Server Error"}), 500

@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
