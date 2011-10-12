#!/usr/bin/env python

import os
import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from util.sessions import Session

# A helper to do the rendering and to add the necessary
# variables for the _base.htm template
def doRender(handler, tname = 'index.htm', values = { }):
  temp = os.path.join(
      os.path.dirname(__file__),
      'templates/' + tname)
  if not os.path.isfile(temp):
    return False

  # Make a copy of the dictionary and add the path and session
  newval = dict(values)
  newval['path'] = handler.request.path
  handler.session = Session()
  if 'username' in handler.session:
     newval['username'] = handler.session['username']

  outstr = template.render(temp, newval)
  handler.response.out.write(outstr)
  return True

class LoginHandler(webapp.RequestHandler):

  def get(self):
    doRender(self, 'loginscreen.htm')

  def post(self):
    self.session = Session()
    acct = self.request.get('account')
    pw = self.request.get('password')
    logging.info('Checking account='+acct+' pw='+pw)

    self.session.delete_item('username')

    if pw == '' or acct == '':
      doRender(
          self,
          'loginscreen.htm',
          {'error' : 'Please specify Account and Password'} )
    elif pw == 'secret':
      self.session['username'] = acct
      doRender(self,'index.htm',{ } )
    else:
      doRender(self,'loginscreen.htm',
            {'error' : 'Incorrect password'} )

class LogoutHandler(webapp.RequestHandler):

  def get(self):
    self.session = Session()
    self.session.delete_item('username')
    doRender(self, 'index.htm')

class MainHandler(webapp.RequestHandler):

  def get(self):
    if doRender(self,self.request.path) :
      return
    doRender(self,'index.htm')

def main():
  application = webapp.WSGIApplication([
     ('/login', LoginHandler),
     ('/logout', LogoutHandler),
     ('/.*', MainHandler)],
     debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
