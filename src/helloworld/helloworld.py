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

import gdata.apps.groups.service

def getAllGroups():
    retorno=""
    ggroups=gdata.apps.groups.service.GroupsService(domain="csq.es")
    ggroups.ClientLogin(username="admin@csq.es", password="L4c0ntr4s3n4d3CSQ", source="googleMarcos")
    
    list= ggroups.RetrieveAllGroups()
    for group in list:
        retorno=retorno+group["groupId"]+ " -> "+ group["emailPermission"]  +"<br>"
    return retorno


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/groups', Groups)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()