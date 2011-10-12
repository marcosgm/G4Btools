#!/usr/bin/env python

import os
import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# A helper to do the rendering and to add the necessary
# variables for the _base.htm template
def doRender(handler, tname = 'index.htm', values = { }):
    if tname == '/' or tname == '' or tname == None:
        tname = 'index.htm'
    temp = os.path.join(
        os.path.dirname(__file__), 
        'templates/' + tname)
    if not os.path.isfile(temp):
      return False

    # Make a copy of the dictionary and add basic values
    newval = dict(values)
    if not 'path' in newval:
        path = handler.request.path
        newval['path'] = handler.request.path

    outstr = template.render(temp, newval)
    handler.response.out.write(outstr)
    return True

class GradeHandler(webapp.RequestHandler):

  def get(self):
    if doRender(self, 'grades.htm'):
       return
    self.response.out.write('Error - grades.htm template not found')

  def post(self):
    hwstr = self.request.get('homework')
    exstr = self.request.get('exam')
    logging.info('Homework='+hwstr+' Exam='+exstr)
    try:
      total = int(hwstr) + int(exstr)
    except:
      total = -1

    if total > 0 :
      if doRender(self,'results.htm',{'total' : total}) :
          return
    else: 
      doRender(self,'grades.htm',{'error' : 'Please enter numeric value'} )

class MainHandler(webapp.RequestHandler):

  def get(self):
    path = self.request.path
    if doRender(self,path) : 
      return
    if doRender(self,'index.htm') : 
      return
    self.response.out.write('Error - unable to find index.htm')

def main():
  application = webapp.WSGIApplication([
     ('/grades', GradeHandler),
     ('/.*', MainHandler)],
     debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
