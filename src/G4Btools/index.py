import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
#gdata API
from googleapi import GoogleApi



class Groups(webapp.RequestHandler):
    def post(self):  
        domain=self.request.get('domain')
        username=self.request.get('username')
        password=self.request.get('password')
        ga=GoogleApi(domain,username,password)
        grupos=ga.getAllGroupsPermissions()
        
        template_values = {
            'domain':domain,
            'username':username,
            'password':password,
            'grupos':grupos
        }

        path = os.path.join(os.path.dirname(__file__), 'groups.html')
        self.response.out.write(template.render(path, template_values))    

class Users(webapp.RequestHandler):
    def post(self):  
        domain=self.request.get('domain')
        username=self.request.get('username')
        password=self.request.get('password')
        ga=GoogleApi(username,password)
        usuarios=ga.getAllUsers()
        
        template_values = {
            'domain':domain,
            'username':username,
            'password':password,
            'usuarios':usuarios
        }

        path = os.path.join(os.path.dirname(__file__), 'users.html')
        self.response.out.write(template.render(path, template_values))   

    
class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
        
        
application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/groups', Groups ),
                                     ('/users', Users )],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()