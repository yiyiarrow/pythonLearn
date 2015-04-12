import web

urls = (
    '/', 'index'
)

class index(object):
    def GET(self):
        return "hello, world!"

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()


