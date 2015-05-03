#!/usr/bin/env python
import web

urls = (
    '/', 'index',
    '/movie/(\d+)', 'movie',
)

render = web.template.render('templates/')

db = web.database(dbn='sqlite', db='MovieSite.db')

class index(object):
    def GET(self):
        movies = db.select('movie') 
        return render.index(movies)
    def POST(self):
        data = web.input()
        condition = r'title like "%' + data.title + r'%"'
        movies = db.select('movie', where=condition)
        return render.index(movies)

class movie(object):
    def GET(self, movie_id):
        movie_id = int(movie_id)
        movie = db.select('movie', where = 'id=$movie_id', vars=locals())[0]
        return render.movie(movie)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
