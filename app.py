import requests
from flask import Flask, render_template, request, session, redirect, url_for
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'

API_KEY = '38deafdd9f5461f328c1ff13ca2d9e6f'  
BASE_URL = 'https://api.openweathermap.org/data/2.5/'

@app.route("/", methods=["GET", "POST"])
def home():
    lang = session.get('lang', 'en')
    
    city = request.args.get('city')
    weather_data = {}

    if city:
        current_url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric&lang={lang}"
        response = requests.get(current_url)
        current_data = response.json()

        if current_data.get('cod') != '404':
            weather_data['city'] = current_data['name']
            weather_data['country'] = current_data['sys']['country']
            weather_data['temperature'] = current_data['main']['temp']
            weather_data['description'] = current_data['weather'][0]['description']
            weather_data['icon'] = current_data['weather'][0]['icon']

            forecast_url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric&lang={lang}"
            forecast_response = requests.get(forecast_url)
            forecast_data = forecast_response.json()

            weather_data['forecast'] = []

            for item in forecast_data['list'][::8]:  
                day_data = {
                    'date': item['dt_txt'],
                    'temp': item['main']['temp'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon']
                }
                weather_data['forecast'].append(day_data)

    return render_template("index.html", weather_data=weather_data, city=city, lang=lang)


@app.route("/set_language/<lang>", methods=["GET"])
def set_language(lang):
    session['lang'] = lang
    return redirect(url_for('home', lang=lang))  


if __name__ == "__main__":
    app.run(debug=True)
