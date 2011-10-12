import os
import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from util.sessions import Session
from google.appengine.ext import db
from google.appengine.api import memcache

# A Model for a User
class User(db.Model):
  account = db.StringProperty()
  password = db.StringProperty()
  name = db.StringProperty()
  created = db.DateTimeProperty(auto_now=True)
  
# A Model for a ChatMessage
class ChatMessage(db.Model):
  user = db.ReferenceProperty()
  text = db.StringProperty()
  created = db.DateTimeProperty(auto_now=True)

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
    self.session.delete_item('userkey')

    if pw == '' or acct == '':
      doRender(
          self,
          'loginscreen.htm',
          {'error' : 'Please specify Account and Password'} )
      return

    que = db.Query(User)
    que = que.filter('account =',acct)
    que = que.filter('password = ',pw)

    results = que.fetch(limit=1)

    if len(results) > 0 :
      user = results[0]
      self.session['userkey'] = user.key()
      self.session['username'] = acct
      doRender(self,'index.htm',{ } )
    else:
      doRender(
          self,
          'loginscreen.htm',
          {'error' : 'Incorrect password'} )

class ApplyHandler(webapp.RequestHandler):

  def get(self):
    doRender(self, 'applyscreen.htm')

  def post(self):
    self.session = Session()
    name = self.request.get('name')
    acct = self.request.get('account')
    pw = self.request.get('password')
    logging.info('Adding account='+acct)

    if pw == '' or acct == '' or name == '':
      doRender(
          self,
          'applyscreen.htm',
          {'error' : 'Please fill in all fields'} )
      return

    # Check if the user already exists
    que = db.Query(User).filter('account =',acct)
    results = que.fetch(limit=1)

    if len(results) > 0 :
      doRender(
          self,
          'applyscreen.htm',
          {'error' : 'Account Already Exists'} )
      return

    # Create the User object and log the user in
    newuser = User(name=name, account=acct, password=pw);
    pkey = newuser.put();
    self.session['username'] = acct
    self.session['userkey'] = pkey
    doRender(self,'index.htm',{ })

class ChatHandler(webapp.RequestHandler):

  def get(self):
    doRender(self,'chatscreen.htm')

  def post(self):
    self.session = Session()
    if not 'userkey' in self.session:
      doRender(
          self,
          'chatscreen.htm',
          {'error' : 'Must be logged in'} )
      return

    msg = self.request.get('message')
    if msg == '':
      doRender(
          self,
          'chatscreen.htm',
          {'error' : 'Blank message ignored'} )
      return

    newchat = ChatMessage(user = self.session['userkey'], text=msg)
    newchat.put();
    doRender(self,'chatscreen.htm')

class MessagesHandler(webapp.RequestHandler):

  def get(self):
    que = db.Query(ChatMessage).order('-created');
    chat_list = que.fetch(limit=10)
    doRender(self, 'messagelist.htm', {'chat_list': chat_list})

class LogoutHandler(webapp.RequestHandler):

  def get(self):
    self.session = Session()
    self.session.delete_item('username')
    self.session.delete_item('userkey')
    doRender(self, 'index.htm')
    
# A quick way to clean up the data models and log out all users
# app.yaml insures that only the app owner can call this
class ResetHandler(webapp.RequestHandler):
  def get(self):

    memcache.flush_all()
    
    while True:
        q = db.GqlQuery("SELECT __key__ FROM User")
        results = q.fetch(1000)
        if ( len(results) < 1 ) : break
        db.delete(results)

    while True :
        q = db.GqlQuery("SELECT __key__ FROM ChatMessage")
        results = q.fetch(1000)
        if ( len(results) < 1 ) : break
        db.delete(results)
        
    self.response.out.write('Reset Complete. <a href="/">Go Back</a>.')


class MainHandler(webapp.RequestHandler):

  def get(self):
    if doRender(self,self.request.path) :
      return
    doRender(self,'index.htm')

def main():
  application = webapp.WSGIApplication([
     ('/login', LoginHandler),
     ('/apply', ApplyHandler),
     ('/chat', ChatHandler),
     ('/messages', MessagesHandler),
     ('/reset', ResetHandler),
     ('/logout', LogoutHandler),
     ('/.*', MainHandler)],
     debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
