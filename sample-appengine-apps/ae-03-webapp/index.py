import logging
import wsgiref.handlers
from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):

  formstring = '''<form method="post" action="/">
<p>Enter Guess: <input type="text" name="guess"/></p>
<p><input type="submit"></p>
</form>'''

  def get(self):
    self.response.out.write('<p>Good luck!</p>\n')
    self.response.out.write(self.formstring)

  def post(self):
    stguess = self.request.get('guess')
    logging.info('User guess='+stguess)
    try:
      guess = int(stguess)
    except:
      guess = -1
    
    answer = 42
    if guess == answer:
      msg = 'Congratulations'
    elif guess < 0 :
      msg = 'Please provide a number guess'
    elif guess < answer:
      msg = 'Your guess is too low'
    else:
      msg = 'Your guess is too high'
    
    self.response.out.write('<p>Guess:'+stguess+'</p>\n')
    self.response.out.write('<p>'+msg+'</p>\n')
    self.response.out.write(self.formstring)

def main():
  application = webapp.WSGIApplication(
      [('/.*', MainHandler)],
      debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
