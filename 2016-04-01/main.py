import webapp2
import logging
from webapp2_extras import sessions

import oauth
import utilities

#A unique private key, to be used when generating Anti-CSRF tokens
privateAppKey = '20160301'

#Redirection URI after authentication and approval by user
#	the Authorization grant is sent to this URI
redirect_uri = 'https://cbtoauth-1235.appspot.com/oauthcallback'

#--------------------------------------------------------------------------
#An extended webapp2 RequestHandler that includes session storage
# See documentation here:  https://webapp-improved.appspot.com/api/webapp2_extras/sessions.html
#--------------------------------------------------------------------------
class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()


#--------------------------------------------------------------------------
#Render a simple login choice page.  This should be templated in HTML with
#	the template language of your choice   
#--------------------------------------------------------------------------	
class MainPage(BaseHandler):
    def get(self):

        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<html><body>')
        self.response.write('<h3><a href="/signin?provider=google">Sign in with Google</a></h3>')
        self.response.write('</body></html>')

#--------------------------------------------------------------------------
#Handle a sign-in request.  The chosen provider is passed as a querystring
#--------------------------------------------------------------------------
class SignIn(BaseHandler):
	def get(self):
		
		#Extract the chosen provider from the querystring
		provider = self.request.get('provider')		
		
		#Generate a unique state variable
		stateObj = utilities.generate_state_parameter(privateAppKey)

		#Store the state in our session so it can be validated on callback	
		#Attach the chosen provider so we can reference it on callback	
		stateToken = stateObj['state'] + 'Provider' + provider
		self.session['state'] = stateToken

		#Get the appropriate URL
		authUrl = oauth.SignIn(provider, redirect_uri, stateToken)
		logging.info(authUrl)
		return self.redirect(authUrl)


#--------------------------------------------------------------------------
#Callback URI after user allows or denies request
#--------------------------------------------------------------------------
class OAuthCallback(BaseHandler):
    def get(self):
        #Extract the provider from the State token (we used the word 'Provider' as a seperator)
        base, provider = self.session.get('state').split('Provider')

        #Just send the relevant information to the OAuth library
        result = oauth.OAuthCallback(self.request, self.session.get('state'), provider, redirect_uri)
        
        #Was there an error (such as denied access) during grant request?
        if (result['error'] == True):            
            self.response.write('<html><body>')
            self.response.write('Error during Authorization Grant:' + result['errorText'])
            self.response.write('<h3><a href="/">Return Home</a></h3>')
            self.response.write('</body></html>')
        #No error, so we should have our access and refresh tokens now as well 
        #as a user identity (email address)
        else:
            logging.info(result['accessToken'])
            logging.info(result['refreshToken'])
            self.response.write('<html><body>')
            self.response.write('Succes!')
            self.response.write('<h3>Hello </h3>' + result['userEmail'])
            self.response.write('</body></html>')
        


#Webapp2 Route Handler.  Ties back to Routing in app.yaml
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': privateAppKey,
}

app = webapp2.WSGIApplication([
	('/signin', SignIn),
    ('/oauthcallback', OAuthCallback),
    ('/', MainPage)
],config=config, debug=True)
