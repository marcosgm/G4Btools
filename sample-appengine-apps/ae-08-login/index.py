
import os
import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# A helper to do the rendering and to add the necessary
# variables for the _base.htm template
def doRender(handler, tname = 'index.htm', values = { }):
  temp = os.path.join(
      os.path.dirname(__file__), 
      'templates/' + tname)
  if not os.path.isfile(temp):
    return False

  # Make a copy of the dictionary and add the path
  newval = dict(values)
  newval['path'] = handler.request.path

  outstr = template.render(temp, newval)
  handler.response.out.write(outstr)
  return True

class LoginHandler(webapp.RequestHandler):

  def get(self):
    doRender(self, 'loginscreen.htm')

  def post(self):
    acct = self.request.get('account')
    pw = self.request.get('password')
    logging.info('Checking account='+acct+' pw='+pw)

    if pw == '' or acct == '':
      doRender(
          self,
          'loginscreen.htm',
          {'error' : 'Please specify Account and Password'} )
    elif pw == 'secret':
      doRender(self,'loggedin.htm',{ } )
    else:
      doRender(
          self,
          'loginscreen.htm',
          {'error' : 'Incorrect password'} )

class MainHandler(webapp.RequestHandler):

  def get(self):
    if doRender(self,self.request.path) : 
      return
    doRender(self,'index.htm')

def main():
  application = webapp.WSGIApplication([
     ('/login', LoginHandler),
     ('/.*', MainHandler)],
     debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
