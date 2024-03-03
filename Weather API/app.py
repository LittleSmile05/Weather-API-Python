from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

def get_weather(city):
    api_key = os.getenv("API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_info = {
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "icon": data["weather"][0]["icon"]
        }
        return weather_info, None
    else:
        return None, "City not found or API key invalid."

@app.route('/')
def index():
    return render_template('index.html', weather=None, error=None)

@app.route('/weather')
def weather():
    city = request.args.get('city')
    weather_info, error = get_weather(city)
    return render_template('index.html', weather=weather_info, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
