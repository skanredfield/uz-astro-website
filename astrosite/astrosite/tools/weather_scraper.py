import datetime
import requests
import time
import sys

from schedule import every, repeat, run_pending

import os, sys
proj_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
sys.path.append(proj_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'astrosite.settings'
import django
django.setup()
from weather_monitor.models import WeatherData
# from django.apps import apps

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
HEADERS = {'User-Agent': USER_AGENT,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

is_running = False

def get_weather_data():
    link = "https://weather.deepskychile.com/curdata.tmp"
    f = requests.get(link, headers=HEADERS)
    return f.text.split('\n')

def save_weather_data():
    data = get_weather_data()
    model = WeatherData()
    model.reading_date = datetime.datetime.now(datetime.timezone.utc)
    model.cwinfo = data[1].split('=')[1]
    model.clouds_level = float(data[2].split('=')[1])
    model.temperature = float(data[3].split('=')[1])
    model.wind_level = int(data[4].split('=')[1])
    model.wind_gust_level = int(data[5].split('=')[1])
    model.rain_level = int(data[6].split('=')[1])
    model.light_level = int(data[7].split('=')[1])
    model.roof_safe_to_open = True if int(data[8].split('=')[1]) == 1 else False
    model.weather_permits_observations = True if int(data[9].split('=')[1]) == 1 else False
    model.humidity_level = int(data[10].split('=')[1])
    model.dew_point = float(data[11].split('=')[1])
    model.save()
    print('Saved weather data ', model.reading_date)

def start_scraper():
    global is_running
    is_running = True
    every().minute.do(save_weather_data)

    while is_running:
        run_pending()
        time.sleep(1)

def stop_scraper():
    global is_running
    is_running = False

def is_running():
    global is_running
    return is_running

if __name__ == '__main__':
    globals()[sys.argv[1]]()
