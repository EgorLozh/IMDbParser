import csv

import requests
from bs4 import BeautifulSoup as BS

import timeit


made_correct = lambda s: s.strip().replace('\n','').replace(',',";").replace('\r','')
headers = {"Accept-Language": "en-US,en;q=0.5"}

def get_name(movie):
    try:
        result = made_correct(movie.select_one('h3.lister-item-header a').text).replace(' ', '_')
    except:
        result = ''
    return result

def get_year(movie):
    try:
        result = made_correct(movie.select('h3.lister-item-header span')[1].text[-5:-1])
    except:
        result = ''
    return result

def get_runtime(movie):
    try:
        result = made_correct(movie.select_one('span.runtime').text[:-4])
    except:
        result = ''
    return result

def get_ganre(movie):
    try:
        result = made_correct(movie.select_one('span.genre').text.replace(' ',''))
    except:
        result = ''
    return result

def get_rating(movie):
    try:
        result = made_correct(movie.select_one('div.ratings-bar div strong').text)
    except:
        result = ''
    return result

def get_description(movie):
    try:
        result = made_correct(movie.select('p.text-muted')[1].text)
    except:
        result = ''
    if 'Add a Plot' in result:
        result = ''
    return result

def get_data(r):
    html = BS(r.text, 'html.parser')
    movies_data = []
    movie_data = dict()
    for movie in html.select('.lister-item-content'):
        movie_data = {
            'name': get_name(movie),
            'year': get_year(movie),
            'runtime': get_runtime(movie),
            'ganre': get_ganre(movie),
            'rating': get_rating(movie),
            'description': get_description(movie)
        }
        movies_data.append(movie_data)
    return movies_data


url = 'https://www.imdb.com'
next_link ='https://www.imdb.com/search/title/?title_type=feature,tv_movie,short&release_date=,2023-01-01'

#1474622
with open('movie_data.csv', 'w', encoding='utf-8', newline = '' ) as data:
    writer = csv.writer(data, delimiter=',', quotechar=' ')
    writer.writerow(['name', 'year', 'runtime', 'ganre', 'rating', 'description'])
    #start_time = timeit.default_timer()
    for i in range(1, 1474622 , 50):
        try:
            r = requests.get(next_link, headers=headers)
        except requests.exceptions.ConnectionError:
            print("Connection Error")
        for movie in get_data(r):
            writer.writerow(movie.values())
        html = BS(r.text, 'html.parser')
        href = list(list(html.select(".desc"))[0].find_all('a', href=True))[-1]["href"]
        next_link = url + href
        print(next_link)
        print(i)

    #print(timeit.default_timer() - start_time)
