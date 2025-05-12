# source.py

from flask import Flask, render_template
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# --- Configuration ---
MODEL_PATH = 'model/trained_model.pkl'
PREDICTION_STEPS = 30  # Number of time steps to forecast

# --- Load the trained model ---
def load_model(path):
    try:
        with open(path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

trained_model = load_model(MODEL_PATH)

# --- Generate predictions ---
def generate_predictions(model, steps):
    if model is None:
        return None, None
    try:
        forecast = model.get_forecast(steps=steps)
        predictions = forecast.predicted_mean
        last_date = model.model.endog.index[-1]
        future_dates = pd.date_range(start=last_date, periods=steps + 1, freq=model.model.index.freq)[1:]
        predictions.index = future_dates
        return predictions, model.model.endog
    except Exception as e:
        print(f"Error generating predictions: {e}")
        return None, None

# --- Create a plot and encode as base64 image ---
def create_plot(historical, predictions):
    plt.figure(figsize=(10, 6))
    plt.plot(historical, label='Historical Data')
    plt.plot(predictions, label='Forecast', color='red')
    plt.title('Energy Consumption Forecast')
    plt.xlabel('Time')
    plt.ylabel('Energy Consumption (MW)')
    plt.legend()
    plt.grid(True)

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

# --- Flask route ---
@app.route('/')
def index():
    predictions, historical = generate_predictions(trained_model, PREDICTION_STEPS)
    if predictions is not None and historical is not None:
        plot_url = create_plot(historical, predictions)
        table_html = predictions.to_frame(name='Predicted Consumption').to_html()
    else:
        plot_url = None
        table_html = "<p>Could not generate predictions.</p>"

    return render_template('index.html', predictions_table=table_html, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
