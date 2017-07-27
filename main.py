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
    isSubLevel = ndb.BooleanProperty()
    user1ID = ndb.StringProperty()
    user2ID = ndb.StringProperty()
    parent_url = ndb.StringProperty()



class Profile(ndb.Model):
    email = ndb.StringProperty()
    userID = ndb.StringProperty()



# We're defining a crux model along with its properties. These will be the "sub-sections", or additional subpoints to our arguments.
class Crux(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.StringProperty()
    onHold = ndb.BooleanProperty()
    onAccept = ndb.BooleanProperty()
    userID = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    discussion_key = ndb.KeyProperty(kind=Discussion)
    subdiscussion_key = ndb.KeyProperty(kind=Discussion)



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
        discussions = Discussion.query().filter(Discussion.isSubLevel == False).order(Discussion.timestamp).fetch()

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
        cruxesByUser1 = Crux.query().filter(Crux.discussion_key == discussion_key, Crux.userID == discussion.user1ID)
        cruxesByUser2 = Crux.query().filter(Crux.discussion_key == discussion_key, Crux.userID == discussion.user2ID)

        user1 = Profile.query().filter(Profile.userID == discussion.user1ID).get()
        user2 = Profile.query().filter(Profile.userID == discussion.user2ID).get()

        template_vars = {
            "user1":user1,
            "user2":user2,
            "current_user": current_user,
            "current_user_id": current_user_id,
            "discussion" : discussion,
            "cruxesByUser1" : cruxesByUser1,
            "cruxesByUser2" : cruxesByUser2,
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

        # If you're at this stage, you've already logged in
        current_user = users.get_current_user()
        current_user_id = current_user.user_id()

        # Making the new comment, the discussion_key tells us which discussion to link the crux to.
        # Default of subdiscussion_key will be none
        crux = Crux(title=title, content=content, onHold= False, onAccept=False, userID = current_user_id, discussion_key = discussion_key, subdiscussion_key = None)

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
            discussionObject = Discussion(title=title, isSubLevel=False, user1ID=user1ID, user2ID=user2ID, parent_url='/').put()
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



#Handler for recursing on cruxes
class RecurseHandler(webapp2.RequestHandler):
    def post(self):
        # check the element provided by the crux's subdiscussion_key
        crux_urlsafe_key = self.request.get("crux_urlsafe_key")

        # grabs the actual crux object from the Key
        crux = ndb.Key(urlsafe=crux_urlsafe_key).get()

        subdiscussion_key = crux.subdiscussion_key

        # if the discussion isn't linked to a subdiscussion:
        if (subdiscussion_key == None or subdiscussion_key == "None"):

            # make a new discussion
            title = self.request.get("crux_title")
            user1ID = self.request.get("user1ID")
            user2ID = self.request.get("user2ID")

            parent_url = '/discussion?key=' + str(crux.discussion_key.urlsafe())

            # Add the subdiscussion to the list:
            subDiscussionObject = Discussion(title=title, isSubLevel=True, user1ID=user1ID, user2ID=user2ID, parent_url=parent_url)

            # update the subdiscussion to the database
            subDiscussionObject.put()

            # The subdiscussion_key will be a key string.
            subdiscussion_urlsafe_key = subDiscussionObject.key.urlsafe()

            # updates the crux subdiscussion_key with the actual Key object associated with the subdiscussion key string
            crux.subdiscussion_key = ndb.Key(urlsafe=subdiscussion_urlsafe_key)
            crux.put()

            # new URL to the new subdiscussion
            url = '/discussion?key=' + str(subdiscussion_urlsafe_key)
            # Grabbing the new subdiscussion url and passing it in
            self.redirect(url)

        else:
            subdiscussion_urlsafe_key = crux.subdiscussion_key.urlsafe()
            url = '/discussion?key=' + str(subdiscussion_urlsafe_key)
            self.redirect(url)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/discussion', DiscussionHandler),
    ('/newcrux', NewCruxHandler),
    ('/creatediscussion', CreateDiscussionHandler),
    ('/discussiononhold', OnHoldHandler),
    ('/onhold', OnHoldHandler),
    ('/onaccept', OnAcceptHandler),
    ('/recurse', RecurseHandler),
], debug=True)
