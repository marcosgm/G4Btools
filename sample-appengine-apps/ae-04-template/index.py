import os
import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):

  def get(self):
    temp = os.path.join(
        os.path.dirname(__file__), 
        'templates/index.htm')
    outstr = template.render(
        temp, 
        {'hint': 'Good luck!'})
    self.response.out.write(outstr)

  def post(self):
    stguess = self.request.get('guess')
    logging.info('POST stguess='+str(stguess))
    msg = ''
    guess = -1
    try:
      guess = int(stguess)
    except:
      guess = -1

    answer = 42
    if guess == answer:
      msg = 'Congratulations'
    elif guess < 0 :
      msg = 'Please provide a number'
    elif guess < answer:
      msg = 'Your guess is too low'
    else:
      msg = 'Your guess is too high'

    temp = os.path.join(
        os.path.dirname(__file__), 
        'templates/guess.htm')
    outstr = template.render(
        temp, 
        {'hint': msg, 'oldguess': stguess})
    self.response.out.write(outstr)

def main():
  application = webapp.WSGIApplication(
      [('/.*', MainHandler)],
      debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
