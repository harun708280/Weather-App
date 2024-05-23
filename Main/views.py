from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime

def cityView(request):
    appid = 'cb30459d616fae7eae86613bd39704b1'
    URL = 'https://api.openweathermap.org/data/2.5/weather'

    if request.method == 'POST' and 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Rangpur'
    
    params = {'q': city, 'appid': appid, 'units': 'metric'}
    try:
        response = requests.get(url=URL, params=params)
        response.raise_for_status()
        res = response.json()
        
        description = res['weather'][0]['description']
        icon_code = res['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        temp = res['main']['temp']
        day = datetime.date.today()
        
        context = {
            'city': city,
            'description': description,
            'icon_url': icon_url,
            'temp': temp,
            'day': day,
        }
    except requests.exceptions.RequestException as e:
        context = {
            'error': 'Error fetching weather data',
        }
    except (KeyError, IndexError) as e:
        context = {
            'error': 'Error processing weather data',
        }

    return render(request, 'index.html', context)
