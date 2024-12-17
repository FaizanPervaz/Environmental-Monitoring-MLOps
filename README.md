# Environmental-Monitoring-MLOps
A comprehensive MLOps project for monitoring environmental data, predicting pollution trends, and visualizing key metrics. This repository integrates DVC for data management, MLflow for model tracking, and Prometheus with Grafana for monitoring a Flask-based prediction API.
---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Details](#project-details)
  - [Task 1: Managing Environmental Data with DVC](#task-1-managing-environmental-data-with-dvc)
  - [Task 2: Pollution Trend Prediction with MLflow](#task-2-pollution-trend-prediction-with-mlflow)
  - [Task 3: Monitoring and Live Testing](#task-3-monitoring-and-live-testing)
- [Results](#results)
- [Technologies Used](#technologies-used)
- [Contributors](#contributors)
- [License](#license)

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

## Architecture

![Architecture Diagram](https://via.placeholder.com/800x400)  
*Diagram illustrating the data collection, processing, prediction, and monitoring flow (Replace this placeholder with your actual diagram).*

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
