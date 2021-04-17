import json
from fuzzywuzzy import fuzz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# coding=utf-8


def contains(list, movie):
    for x in list:
        if('name' in x.keys() and 'name' in movie.keys()):
            if (fuzz.ratio(x['name'].upper(), movie['name'].upper()) >= 90):
                return x
    return False

def add(movie,movies):
    url = movie['url'] if 'url' in movie.keys() else ''
    movie['url'] = []
    if(url):
        movie['url'].append(url)
    name = movie['name'] if 'name' in movie.keys() else ''
    movie['name'] = name
    image = movie['image'] if 'image' in movie.keys() else ''
    movie['image'] = image
    description = movie['description'] if 'description' in movie.keys() else ''
    movie['description'] = description
    duration = movie['duration'] if 'duration' in movie.keys() else ''
    movie['duration'] = duration
    genre = movie['genre'] if 'genre' in movie.keys() else []
    movie['genre'] = genre

    director = movie['director'] if 'director' in movie.keys() else []
    movie['director'] = director
    #SI ES UNO SOLO GENERO UN ARRAY Y LO AGREGO (POR SI EN LOS DEMAS LINKS TIENE MAS DE UNO)
    if (not isinstance(movie['director'], list)):
        director = movie['director']
        movie['director'] = []
        movie['director'].append(director)

    actor = movie['actor'] if 'actor' in movie.keys() else []
    movie['actor'] = actor
    # SI ES UNO SOLO GENERO UN ARRAY Y LO AGREGO (POR SI EN LOS DEMAS LINKS TIENE MAS DE UNO)
    if (not isinstance(movie['actor'], list)):
        actor = movie['actor']
        movie['actor'] = []
        movie['actor'].append(actor)

    creator = movie['creator'] if 'creator' in movie.keys() else []
    movie['creator'] = creator
    # SI ES UNO SOLO GENERO UN ARRAY Y LO AGREGO (POR SI EN LOS DEMAS LINKS TIENE MAS DE UNO)
    if (not isinstance(movie['creator'], list)):
        actor = movie['creator']
        movie['creator'] = []
        movie['creator'].append(creator)

    rating = movie['aggregateRating'] if 'aggregateRating' in movie.keys() else {}
    movie['aggregateRating'] = rating

    review = movie['review'] if 'review' in movie.keys() else []
    movie['review'] = review
    # SI ES UNO SOLO GENERO UN ARRAY Y LO AGREGO POR SI EN LOS DEMAS LINKS TIENE MAS DE UNO
    if (not isinstance(movie['review'], list)):
        review = movie['review']
        movie['review'] = []
        movie['review'].append(review)

    movies.append(movie);


def unify(movie1, movie2):
    if('url' in movie2.keys()):
        movie['url'].append(movie2['url'])
    if(not movie1['name']):
        movie1['name'] = movie2['name']
    if (not movie1['image']):
        movie1['image'] = movie2['image']
    if (not movie1['description']):
        movie1['description'] = movie2['description']
    if (not movie1['duration']):
        movie1['duration'] = movie2['duration']

    movie1['genre'] = list(set(movie1['genre'] + movie2['genre']))

    if("director" in movie2.keys()):
        if (isinstance(movie2['director'], list)):
            for d in movie2['director']:
                if(not contains(movie1['director'], d)):
                    movie1['director'].append(d)
        else:
            if (not contains(movie1['director'], movie2['director'])):
                movie1['director'].append(movie2['director'])

    if ("actor" in movie2.keys()):
        if (isinstance(movie2['actor'], list)):
            for d in movie2['actor']:
                if (not contains(movie1['actor'], d)):
                    movie1['actor'].append(d)
        else:
            if (not contains(movie1['actor'], movie2['actor'])):
                movie1['actor'].append(movie2['actor'])

    if ("creator" in movie2.keys()):
        if (isinstance(movie2['creator'], list)):
            for d in movie2['creator']:
                if (not contains(movie1['creator'], d)):
                    movie1['creator'].append(d)
        else:
            if (not contains(movie1['creator'], movie2['creator'])):
                movie1['creator'].append(movie2['creator'])

    if ("review" in movie2.keys()):
        if (isinstance(movie2['review'], list)):
            for r in movie2['review']:
                movie1['review'].append(r)
        else:
            movie1['review'].append(movie2['review'])



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    DRIVER_PATH = '/Users/pilar/Desktop/SCRAPPER/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    sources = ['https://www.imdb.com/title/tt7126948/',
               'https://www.rottentomatoes.com/m/wonder_woman_1984',
               'https://www.metacritic.com/movie/wonder-woman-1984',
               'https://www.ecartelera.com/peliculas/wonder-woman-1984/']

    movies = []

    for source in sources:
        driver.get(source)
        data = driver.find_element_by_xpath('//script[@type="application/ld+json"]')
        data = data.get_attribute('innerHTML')
        data = json.loads(data, strict=False)

        movie = contains(movies, data)
        if (movie != False):
            unify(movie, data)
        else:
            add(data, movies)

    with open('data.json', 'w') as outfile:
        y = list(movies)
        print(y)
        json.dump(y, outfile)

    driver.quit()


