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
from gdata.apps.emailsettings import client
from gdata.apps.groups import service

def printFeed(feed, printer):
    '''
    Prints out the contents of a feed to the console and puts items into a python list [].
    Takes Gdata XML feed as first argument, and 'printer' as second argument.
    If printer = True, the function will print results to the console. Straight from Google documentation.
    '''
    if(len(feed.entry) == 0):
        print 'No entries in feed.\n'
        
    feedItems = []
    for i, entry in enumerate(feed.entry):
        if printer == True:
            print '%s %s' % (i+1, entry.title.text.encode('UTF-8'))
        else:
            pass
        feedItems.append(entry.title.text.encode('UTF-8'))
    return feedItems

def getAllGroups(domain,username,password):
    retorno=""
    ggroups=service.GroupsService(domain=domain)
    ggroups.ClientLogin(username=username, password=password, source="G4Btools")
    list=ggroups.RetrieveAllGroups()
    for group in list:
        retorno=retorno+group["groupId"]+ " -> "+ group["emailPermission"]  +"<br>"
    return retorno

def getAllMailSignatures(domain,username,password):
    retorno=""
    serviceclient = gdata.apps.service.AppsService(username, domain, password)
    serviceclient.ProgrammaticLogin()
#    service.RetrieveAllUsers() esto devuelve un monton de feeds como este: http://code.google.com/intl/es-ES/googleapps/domain/gdata_provisioning_api_v2.0_reference_python.html
#(NOTA: maximo 100 resultados, hay que paginar http://code.google.com/intl/es-ES/googleapps/domain/gdata_provisioning_api_v2.0_reference.html#Results_Pagination)
#===============================================================================
# <ns0:entry>
# <ns2:name familyName="CSQ" givenName="wissale" />
# <ns0:category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/apps/2006#user" />
# <ns0:id>https://apps-apis.google.com/a/feeds/csq.es/user/2.0/wissale</ns0:id>
# <ns0:updated>1970-01-01T00:00:00.000Z</ns0:updated>
# <ns2:quota limit="25600" />
# <ns3:feedLink href="https://apps-apis.google.com/a/feeds/csq.es/nickname/2.0?username=wissale" rel="http://schemas.google.com/apps/2006#user.nicknames" />
# <ns3:feedLink href="https://apps-apis.google.com/a/feeds/csq.es/emailList/2.0?recipient=wissale%40csq.es" rel="http://schemas.google.com/apps/2006#user.emailLists" />
# <ns0:title type="text">wissale</ns0:title>
# <ns0:link href="https://apps-apis.google.com/a/feeds/csq.es/user/2.0/wissale" rel="self" type="application/atom+xml" />
# <ns0:link href="https://apps-apis.google.com/a/feeds/csq.es/user/2.0/wissale" rel="edit" type="application/atom+xml" />
# <ns2:login admin="false" agreedToTerms="true" changePasswordAtNextLogin="false" ipWhitelisted="false" suspended="false" userName="wissale" />
# </ns0:entry>
# </ns0:feed>
#===============================================================================
#see also http://code.google.com/p/gdata-python-client/wiki/WritingDataModelClasses
#    emailSetting=client.EmailSettingsClient(domain)
#    emailSetting.client_login(email=username, password, source="G4Btools")
#obtenemos la signature accediendo al feed del usuario
#print(emailSetting.get_entry('https://apps-apis.google.com/a/feeds/emailsettings/2.0/csq.es/marcos/signature'))

    userFeed = serviceclient.RetrieveAllUsers()
    items = printFeed(userFeed, printer)
    userDict = {'Users':items}

class Groups(webapp.RequestHandler):
    def post(self):  
        domain=self.request.get('domain')
        username=self.request.get('username')
        password=self.request.get('password')
        grupos=getAllGroups(domain,username,password)
        
        template_values = {
            'domain':domain,
            'username':username,
            'password':password,
            'grupos':grupos
        }

        path = os.path.join(os.path.dirname(__file__), 'groups.html')
        self.response.out.write(template.render(path, template_values))    
    
class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
        
        
application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/groups', Groups )],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()