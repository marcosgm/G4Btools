#!/usr/bin/env python

import os
import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):

  def get(self):
    path = self.request.path
    temp = os.path.join(
        os.path.dirname(__file__),
        'templates/%s' % path)
    if not os.path.isfile(temp):
        temp = os.path.join(
            os.path.dirname(__file__),
           'templates/index.htm')

    outstr = template.render(temp, { 'path': path })
    self.response.out.write(outstr)

def main():
  application = webapp.WSGIApplication(
      [('/.*', MainHandler)],
      debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
