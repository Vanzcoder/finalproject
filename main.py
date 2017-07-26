import webapp2
import jinja2
import os
import datetime

from google.appengine.ext import ndb
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


# We're defining a discussion model, which should house our cruxes and be linked to two users,
class Discussion(ndb.Model):
    title = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    user1ID = ndb.StringProperty()
    user2ID = ndb.StringProperty()
    # We don't yet know what properties a discussion should have, so let's hold off on the properties for now.
class Profile(ndb.Model):
    email = ndb.StringProperty()
    userID = ndb.StringProperty()

# We're defining a crux model along with its properties. These will be the "sub-sections", or additional subpoints to our arguments.
class Crux(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.StringProperty()
    onHold = ndb.BooleanProperty()
    onAccept = ndb.BooleanProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    discussion_key = ndb.KeyProperty(kind=Discussion)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # This is the login information we're currently using, but we might change it later on.
        current_user = users.get_current_user()

        if (current_user == None):
            current_user_id = 'none'
        else:
            current_user_id = current_user.user_id()

        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/')

        userID = current_user_id
        profile_query = Profile.query().filter(Profile.userID == userID)
        currentprofile = profile_query.get()

        if not currentprofile:
            if (current_user == None):
                email = 'none'
            else:
                email = current_user.email()
                profile = Profile(userID=userID, email=email)
                profile.put()

        # On load, we're querying the database for all existing Discussion objects, fetching them, and we're passing them in to Jinja.
        discussions = Discussion.query().order(Discussion.timestamp).fetch()

        # We're passing in information about the user (which we might change) as well as the discussions. But we don't yet know how the discussions will work.
        template = jinja_environment.get_template('templates/home.html')
        template_vars = {
            "current_user": current_user,
            "current_user_id": current_user_id,
            "logout_url": logout_url,
            "login_url": login_url,
            "discussions" : discussions,
            "currentprofile": currentprofile,
        }
        self.response.write(template.render(template_vars))



# This allows us to show discussions from the link on Home
class DiscussionHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        if (current_user == None):
            current_user_id = 'none'
        else:
            current_user_id = current_user.user_id()
        #We grab the urlsafe key we got from HTML
        urlsafe_key = self.request.get("key")

        #We generate the Actual Key from the urlsafe_key, which is only a String
        discussion_key = ndb.Key(urlsafe = urlsafe_key)

        #Using the Key object, we're able to access the entire object.
        #Which then allows us to grab the add'l info like the content and author
        discussion = discussion_key.get()

        #Filtering, ordering, and fetching our cruxes for each discussion.
        cruxes = Crux.query().filter(Crux.discussion_key == discussion_key)
        cruxes = cruxes.order(-Crux.timestamp).fetch()

        template_vars = {
            "current_user": current_user,
            "current_user_id": current_user_id,
            "discussion" : discussion,
            "cruxes" : cruxes,
        }

        template = jinja_environment.get_template('templates/discussion.html')
        self.response.write(template.render(template_vars))


# This allows us to make new cruxes, similar to the comments handler we did in the blog example.
class NewCruxHandler(webapp2.RequestHandler):
    def post(self):
        urlsafe_key = self.request.get("discussion_key")
        title = self.request.get("title")
        content = self.request.get("content")

        #Turn url safe key = key object
        discussion_key = ndb.Key(urlsafe = urlsafe_key)

        #Making the new comment, the discussion_key tells us which discussion to link the crux to.
        crux = Crux(title=title, content=content, onHold= False, discussion_key = discussion_key)

        #Actually putting the object onto our database
        crux.put()

        url = '/discussion?key=' + str(urlsafe_key)

        #Sending the response back:
        self.redirect(url)


# Handler that allows us to create a new discussion
class CreateDiscussionHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        if (current_user == None):
            current_user_id = 'none'
        else:
            current_user_id = current_user.user_id()

        template_vars = {
            "current_user_id": current_user_id,
        }

        template = jinja_environment.get_template('templates/creatediscussion.html')
        self.response.write(template.render(template_vars))
    def post(self):
        # THis allows us to create a new Discussion link on home from the HTML form
        title = self.request.get('title')
        user1ID = self.request.get('user1ID')
        user2email = self.request.get('user2email')

        profile_query = Profile.query().filter(Profile.email == user2email)
        user2 = profile_query.get()
        if not user2:
            self.redirect('/')# ***redirect to error page
        else:
            user2ID = user2.userID
            discussionObject = Discussion(title=title,user1ID=user1ID, user2ID=user2ID).put()
            self.redirect('/')


# Handler for AJAX calls when putting a crux on hold.
class OnHoldHandler(webapp2.RequestHandler):
    def post(self):
        # === 1: Get info from the request. ===
        urlsafe_key = self.request.get('crux_key')

        # === 2: Interact with the database. ===

        # Use the URLsafe key to get the photo from the DB.
        crux = ndb.Key(urlsafe=urlsafe_key).get()

        # Update the boolean
        crux.onHold = not crux.onHold
        crux.onAccept = False

        # Store it in the database, updated
        crux.put()


# Handler for AJAX calls when accepting a crux.
class OnAcceptHandler(webapp2.RequestHandler):
    def post(self):
        # === 1: Get info from the request. ===
        urlsafe_key = self.request.get('crux_key')

        # === 2: Interact with the database. ===

        # Use the URLsafe key to get the photo from the DB.
        crux = ndb.Key(urlsafe=urlsafe_key).get()

        # Update the boolean
        crux.onAccept = not crux.onAccept
        crux.onHold = False

        # Store it in the database, updated
        crux.put()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/discussion', DiscussionHandler),
    ('/newcrux', NewCruxHandler),
    ('/creatediscussion', CreateDiscussionHandler),
    ('/discussiononhold', OnHoldHandler),
    ('/onhold', OnHoldHandler),
    ('/onaccept', OnAcceptHandler),
], debug=True)
