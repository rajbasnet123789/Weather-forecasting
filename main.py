import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Set up the Streamlit app
st.title("Holt-Winters Forecasting App for Min and Max Temperature")
st.write("This app uses pre-trained Holt-Winters models to forecast min and max temperature data.")

# Input random future date
future_date_input = st.text_input(
    "Enter a future date (in the format DD-MM-YYYY):",
    placeholder="e.g., 15-01-2025"
)

# Load the pre-trained models for Min and Max Temperature
try:
    min_model = joblib.load("holt_winters_min_model.joblib")
    max_model = joblib.load("holt_winters_max_model.joblib")
    st.success("Min and Max Temperature Models loaded successfully!")
except FileNotFoundError:
    st.error("Holt-Winters model files not found. Make sure the joblib files are in the same directory.")
    st.stop()

# Set the last training date used in the models (manually or inferred)
model_start_date = datetime(2024, 12, 31)  # Replace with actual last date used in training

if future_date_input:
    try:
        # Parse the future date
        future_date = datetime.strptime(future_date_input, "%d-%m-%Y")
        
        # Validate that the input date is in the future
        if future_date <= model_start_date:
            st.error(f"Please enter a date later than the model's last date ({model_start_date.strftime('%d-%m-%Y')}).")
        else:
            # Calculate the number of steps to forecast for min and max temperature
            forecast_steps = (future_date - model_start_date).days
            
            # Forecast using both models
            min_forecast = min_model.forecast(steps=forecast_steps)
            max_forecast = max_model.forecast(steps=forecast_steps)
            
            # Display forecasted values
            min_forecast_value = min_forecast.iloc[-1]
            max_forecast_value = max_forecast.iloc[-1]
            st.write(f"Forecasted Min Temperature for {future_date.strftime('%d-%m-%Y')}: **{min_forecast_value:.2f}°C**")
            st.write(f"Forecasted Max Temperature for {future_date.strftime('%d-%m-%Y')}: **{max_forecast_value:.2f}°C**")
    
    except ValueError:
        st.error("Invalid date format. Please enter the date in DD-MM-YYYY format.")
