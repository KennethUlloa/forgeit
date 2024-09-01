from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def home():
    weater_forecast = [
        {
            "day": "Monday",
            "temperature": 20,
            "description": "Sunny"
        },
        {
            "day": "Tuesday",
            "temperature": 22,
            "description": "Cloudy"
        },
        {
            "day": "Wednesday",
            "temperature": 18,
            "description": "Rainy"
        }
    ]
    return render_template('index.html', weater_forecast=weater_forecast)
