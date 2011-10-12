import webapp2

import sys


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, WebApp World!')
        for d in sys.path:
            self.response.out.write(d)

app = webapp2.WSGIApplication([('/', MainPage)])