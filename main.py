import webapp2
import jinja2
import os
import datetime

from google.appengine.ext import ndb

from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Crux(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.StringProperty()
    email = ndb.StringProperty()
    post_time = ndb.DateTimeProperty(auto_now_add=True)

class Discussion(ndb.Model):
    author = ndb.StringProperty()
    post_time = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    dicussion_key = ndb.KeyProperty()

#
#     class User:


class MainHandler(webapp2.RequestHandler):
    def get(self):
        discussion_query = Discussion.query().order(Discussion.post_time)
        discussions = discussion_query.fetch()

        current_user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/')

        template = jinja_environment.get_template('templates/home.html')
        template_vars = {
            "current_user": current_user,
            "logout_url": logout_url,
            "login_url": login_url,
            "discussions": discussions,
        }
        self.response.write(template.render(template_vars))

class DiscussionHandler(webapp2.RequestHandler):
    def get(self):
        urlsafe_key = self.request.get('key')
        discussion = ndb.Key(urlsafe=urlsafe_key).get() # urlsafe converts the string into an object
            # the .get fetches the post by using the unique

        # why not this??? Why query one and get the other???
        # discussion = Discussion.query().order(Discussion.post_time).fetch()

        crux_query = Crux.query().order(Crux.post_time)
        cruxes = crux_query.fetch()

        template_vars = {
            "discussions": discussion,
            "cruxes": cruxes,
        }
        template = jinja_environment.get_template('templates/discussion.html')
        self.response.write(template.render(template_vars))

    def post(self):
        title = self.request.get('title')
        content = self.request.get('content')

        current_user = users.get_current_user()
        email = current_user.email()

        crux = Crux(title=title, content=content, email=email)
        crux.put()

        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/discussion', DiscussionHandler),
], debug=True)
