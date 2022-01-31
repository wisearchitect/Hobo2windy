# HOBO Onset -> Windy weather data update
# Copy right 2022 Danial M. Parapari

import requests
import time
import re
from bs4 import BeautifulSoup


windyurl = 'https://stations.windy.com./pws/update/eyJhbGciOiJIUzI1NiIsInR'
windyurl = windyurl + '5cCI6IkpXVCJ9.eyJjaSI6OTI1NjMxLCJpYXQiOjE2NDI4ODcyMzd9.'
windyurl = windyurl + 'C4CMPoruxSxKgh9eBSQvBa4REVgOLJobEC4Atxkwk9Y?'


def get_data():
    url = 'https://www.hobolink.com/p/59be9cf94d55528c8c22e5005402a028'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    datafull = soup.find_all('span', class_='latest-conditions-info-reading')
    data = [dt.get_text() for dt in datafull]
    mbar = data[0]
    temp = data[1]
    rh = data[2]
    dp = data[3]
    wind = data[7]
    gust = data[8]
    rain = data[9]
    tempvar = re.findall(r'\d+', data[10])
    winddirlis = list(map(int, tempvar))
    winddir = str(winddirlis[0])
    output = 'temp=' + temp + '&wind=' + wind + '&winddir=' + winddir
    output = output + '&gust=' + gust + '&rh=' + rh + '&dewpoint=' + dp
    output = output + '&mbar=' + mbar + '&precip=' + rain
    return output


def post_data(url):
    post = requests.get(url)
    return post.text


while True:
    data = get_data()
    url = windyurl + data
    response = post_data(url)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(data)
    print(response)
    print(current_time)
    time.sleep(600)
