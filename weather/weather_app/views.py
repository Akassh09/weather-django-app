from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.


def get_html_content(request):
    
    city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content


def index(request):
    city_weather = None
    if 'city' in request.GET:
        # fetch the weather from Google.
        html_content = get_html_content(request)
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # extract region
        city = soup.find("div", attrs={"id": "wob_loc"}).text
        # extract temperature now
        temp = soup.find("span", attrs={"id": "wob_tm"}).text
        # get the day and hour now
        dayhour = soup.find("div", attrs={"id": "wob_dts"}).text
        # get the actual weather
        desc = soup.find("span", attrs={"id": "wob_dc"}).text

        city_weather = {
            'city': city,
            'temp': temp,
            'dayhour' : dayhour,
            'desc': desc,
        }

    return render(request, 'index.html', {'weather': city_weather})

