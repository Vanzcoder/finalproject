import webapp2
import jinja2
import os
import datetime

from google.appengine.ext import ndb

from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())

class DiscussionHandler(webapp2.RequestHandler):
    def get(self):

        template = jinja_environment.get_template('templates/discussion.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/discussion', DiscussionHandler),
], debug=True)
