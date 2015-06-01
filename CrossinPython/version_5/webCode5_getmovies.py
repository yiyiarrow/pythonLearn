#!/usr/bin/env python
import web
import urllib 
import json
import time
 
movie_ids = []

db = web.database(dbn='sqlite', db='MovieSite.db')

for index in range(0, 250, 50):
    response = urllib.urlopen('http://api.douban.com/v2/movie/top250?start=%d&count=50' % index)
    data_json = response.read()
    data = json.loads(data_json)
    movie250 = data['subjects']
    for movie in movie250:
        movie_ids.append(movie['id'])
        print movie['id'], movie['title']
    time.sleep(3)

def add_movie(data):
    movie = json.loads(data)
    print movie['title']
    db.insert('movie',
        id=int(movie['id']),
        title=movie['title'],
        origin=movie['original_title'],
        url=movie['alt'],
        rating=movie['rating']['average'],
        image_url=movie['images']['large'],
        directors=', '.join([d['name'] for d in movie['directors']]),
        casts=', '.join([c['name'] for c in movie['casts']]),
        year=movie['year'],
        genres=', '.join(movie['genres']),
        countries=', '.join(movie['countries']),
        summary=movie['summary']
    )  
        
         
count = 0
for mid in movie_ids:
    print count, mid
    response = urllib.urlopen('http://api.douban.com/v2/movie/subject/%s' % mid)        
    data_json = response.read()
    add_movie(data_json)
    count += 1
    time.sleep(3)
