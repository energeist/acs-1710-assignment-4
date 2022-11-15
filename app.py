import os
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
from geopy.geocoders import Nominatim

################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('OW_API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather'

################################################################################
## ROUTES
################################################################################

def make_api_call(update_city, params):
    """calls the Openweather API and returns results in JSON format"""
    params['q'] = update_city
    result_json = requests.get(API_URL, params=params).json()
    return result_json


@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

@app.route('/results')
def results():
    """Displays results for current weather conditions."""
    # TODO: Use 'request.args' to retrieve the city & units from the query
    # parameters.
    city = request.args.get("city").strip()
    units = request.args.get("units")

    params = {
    'appid': API_KEY,
    'q': city,
    'units': units 
    }

    def make_api_call(update_city):
        """calls the Openweather API and returns results in JSON format"""
        params['q'] = update_city
        result_json = requests.get(API_URL, params=params).json()
        return result_json

    # TODO: Enter query parameters here for the 'appid' (your api key),
    # the city, and the units (metric or imperial).
    # See the documentation here: https://openweathermap.org/current

    # Uncomment the line below to see the results of the API call!

    # TODO: Replace the empty variables below with their appropriate values.
    # You'll need to retrieve these from the result_json object above.

    # For the sunrise & sunset variables, I would recommend to turn them into
    # datetime objects. You can do so using the `datetime.fromtimestamp()` 
    # function.
    result_json = make_api_call(city)
    pp.pprint(result_json)
    print()
    icon = result_json['weather'][0]['icon']
    image = "https://openweathermap.org/img/wn/"+icon+"@2x.png"
    if result_json['cod'] == '404' or result_json['cod'] == '400':
        context = {
            'passed': False
        }
    else:
        context = {
            'passed': True,
            'date': datetime.now(),
            'city': city,
            'country': result_json['sys']['country'],
            'description': result_json['weather'][0]['description'],
            'temp': result_json['main']['temp'],
            'humidity': result_json['main']['humidity'],
            'wind_speed': result_json['wind']['speed'],
            'sunrise': datetime.fromtimestamp(result_json['sys']['sunrise']),
            'sunset': datetime.fromtimestamp(result_json['sys']['sunset']),
            'units_letter': get_letter_for_units(units),
            'icon': icon,
            'country': result_json['sys']['country']
        }
    return render_template('results.html', **context)

@app.route('/comparison_results')
def comparison_results():
    """Displays the relative weather for 2 different cities."""
    # TODO: Use 'request.args' to retrieve the cities & units from the query
    # parameters.
    city1 = request.args.get("city1").strip()
    city2 = request.args.get("city2").strip()
    units = request.args.get("units")

    params = {
    'appid': API_KEY,
    'q': city1,
    'units': units 
    }

    def make_api_call(update_city):
        """calls the Openweather API and returns results in JSON format"""
        params['q'] = update_city
        result_json = requests.get(API_URL, params=params).json()
        return result_json

    # TODO: Make 2 API calls, one for each city. HINT: You may want to write a 
    # helper function for this!
    result_json = make_api_call(city1)
    print("JSON ONE")
    variable = '        st uff         '
    print(variable)
    variable = variable.strip()
    print(variable)
    print(city1)
    print(city2)
    print(result_json)
    if result_json['cod'] == '404' or result_json['cod'] == '400':
        city_info_1 = {
            'one_passed': False
        }
    else:
        city_info_1 = {
            'one_passed': True,
            'country': result_json['sys']['country'],
            'description1': result_json['weather'][0]['description'],
            'temp': result_json['main']['temp'],
            'humidity': result_json['main']['humidity'],
            'wind_speed': result_json['wind']['speed'],
            'sunrise': datetime.fromtimestamp(result_json['sys']['sunrise']),
            'sunset': datetime.fromtimestamp(result_json['sys']['sunset']),
        }
    result_json = make_api_call(city2)
    print("JSON TWO")
    print()
    print(result_json)
    if result_json['cod'] == '404' or result_json['cod'] == '400':
        city_info_2 = {
            'two_passed': False
        }
    else:
        city_info_2 = {
            'two_passed': True,
            'country': result_json['sys']['country'],
            'description': result_json['weather'][0]['description'],
            'temp': result_json['main']['temp'],
            'humidity': result_json['main']['humidity'],
            'wind_speed': result_json['wind']['speed'],
            'sunrise': datetime.fromtimestamp(result_json['sys']['sunrise']),
            'sunset': datetime.fromtimestamp(result_json['sys']['sunset']),
        } 
    # TODO: Pass the information for both cities in the context. Make sure to
    # pass info for the temperature, humidity, wind speed, and sunset time!
    # HINT: It may be useful to create 2 new dictionaries, `city1_info` and 
    # `city2_info`, to organize the data.
    context = {
        'city1': city1,
        'city2': city2,
        'date': datetime.now(),
        'city_1_info': city_info_1,
        'city_2_info': city_info_2,
        'units_letter': get_letter_for_units(units)
    }
    return render_template('comparison_results.html', **context)

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
