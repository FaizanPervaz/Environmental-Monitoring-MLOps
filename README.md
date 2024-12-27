# Environmental-Monitoring-MLOps
A comprehensive MLOps project for monitoring environmental data, predicting pollution trends, and visualizing key metrics. This repository integrates DVC for data management, MLflow for model tracking, and Prometheus with Grafana for monitoring a Flask-based prediction API.
---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Details](#project-details)
  - [Task 1: Managing Environmental Data with DVC](#task-1-managing-environmental-data-with-dvc)
  - [Task 2: Pollution Trend Prediction with MLflow](#task-2-pollution-trend-prediction-with-mlflow)
  - [Task 3: Monitoring and Live Testing](#task-3-monitoring-and-live-testing)
- [Technologies Used](#technologies-used)
---

## Project Overview

This project automates the process of collecting, managing, and processing environmental data to predict pollution trends and monitor system performance in real-time. 

The pipeline integrates:
- **Data Versioning**: DVC to manage real-time data streams.
- **Model Tracking**: MLflow to log and manage model experiments.
- **Monitoring**: Prometheus and Grafana to monitor API performance and system metrics.

The system is designed to handle real-world environmental data and ensure scalability using Docker containers.

---

## Features

- Real-time data collection from APIs like OpenWeatherMap and IQAir.
- Automated data versioning with DVC.
- Time-series prediction models (ARIMA, LSTM) for forecasting pollution trends.
- Experiment tracking with MLflow.
- Live API for predictions deployed using Flask.
- Real-time monitoring with Prometheus and Grafana dashboards.

---

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.9+
- Docker and Docker Compose
- DVC
- MLflow
- Prometheus and Grafana

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/FaizanPervaz/Environmental-Monitoring-MLOps.git
   cd Environmental-Monitoring-MLOps

2. pip install -r requirements.txt
3. dvc init
4. dvc remote add -d myremote <remote-storage-url>
5. python fetch_data.py
6. Run temp.ipynb file block by block and train models
7. python app.py
8. Start Prometheus and Grafana:
   Configure Prometheus with prometheus.yml.
   Import the Grafana dashboard using the provided JSON file.



## Usuage
---
1. Run Data Collection:
    python fetch_data.py or create bat file for it
2. Track Data with DVC:
     1. dvc add data/
     2. dvc commit
     3. dvc push
3. Train models using ipynb file
4. Run Predictions via API, I used Postman for Post Requesting:
    - Start the API: python app.py
    - Make predictions by sending a POST request :
  ```bash
   {
  "temperature": 25.5,
  "humidity": 60,
  "weather": 2,
  "hour": 14,
  "day": 10,
  "month": 12,
  "co": 0.5,
  "no2": 0.02,
  "o3": 0.03,
  "pm2_5": 35,
  "pm10": 50,
  "PRCP": 0.1,
  "TAVG": 25,
  "TMAX": 28,
  "TMIN": 22
}
```
6. Visualize Metrics:
   - Open Grafana at http://localhost:3000.
   - View real-time dashboards for predictions and system performance.


## Project Details
---

### Task 1: Managing Environmental Data with DVC
#### Data Sources:
- **OpenWeatherMap API**: Weather and pollution data.
- **IQAir API**: Air quality data.
- **NOAA**: Historical weather data.

#### Key Steps:
1. **Initialize DVC Repository**: Version control for collected data.
2. **Automate Data Fetching**: Python scripts and cron jobs.
3. **Track and Push Data**: Use DVC to version and push data to remote storage.

---

### Task 2: Pollution Trend Prediction with MLflow
#### Modeling:
- **ARIMA**: Univariate time-series forecasting.
- **LSTM**: Multi-step pollution prediction.

#### Key Steps:
1. **Preprocess Data**:
   - Handle missing values.
   - Merge datasets.
   - Engineer features.
2. **Model Training**:
   - Hyperparameter tuning.
   - Log experiments in MLflow.
3. **Deploy Best Model**: Serve predictions through a Flask API.

---

### Task 3: Monitoring and Live Testing
#### Monitoring:
- **Prometheus**: Scrapes API metrics (latency, request count, prediction accuracy).
- **Grafana**: Visualizes system performance and prediction trends.

#### Live Testing:
1. **Continuous Testing**: Real-time API data testing.
2. **Prediction Comparison**: Compare real-time predictions with ground truth values.

## Technologies Used
---
- Languages: Python
- Versioning: DVC, Git
- Modeling: TensorFlow, Keras, statsmodels
- Deployment: Flask, Docker
- Monitoring: Prometheus, Grafana
