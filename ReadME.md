# House Price Prediction Application

This is my engineering project on house price prediction using a dataset from Kaggle. The application is a web application built with Django for the backend and Vue.js for the frontend. The backend is containerized using Docker.

## Features
- Predict house prices based on various features
- User-friendly interface
- Data visualization

## Installation

### Prerequisites
Make sure you have Docker installed on your machine.

### Setting Up the Backend

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
2. **Build the Docker image for the backend:**
   ```bash
   docker build -t house-price-prediction-backend .
3. **Run the Docker container for the backend:**
    ```bash
   docker run -p 8000:8000 house-price-prediction-backend

### Setting Up the Frontend
1. **Navigate to the frontend directory:**
    ```bash
    cd <frontend-directory>
2. **Install dependencies for Vue.js:**
    ```bash
    npm install
3. **Run the Vue development server:**
    ```bash
    npm run serve


### Ensuring Database Connectivity
To make sure the Django backend connects to the PostgreSQL database, ensure you have the following settings in your Django settings file (`settings.py`):
