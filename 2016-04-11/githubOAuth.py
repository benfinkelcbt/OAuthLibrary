import urllib
import urllib2
import json

client_id = '9dfc28bfe6e5f1fc59b8'
client_secret = '6061e9d503b4d13b064e6b6758c593eeb00096d4'

#The endpoints for OAuth flow
endpoint_auth = 'https://github.com/login/oauth/authorize'
endpoint_access = 'https://github.com/login/oauth/access_token'
endpoint_email = 'https://api.github.com/user/emails'

#The querystring parameters for Authorization
query_auth = {			
			'client_id' : client_id,
			'redirect_uri' : '',
			'scope' : 'user:email',
			'state' : ''
			}

query_access = {
		'code' : '',
		'client_id' : client_id,
		'client_secret' : client_secret,
		'redirect_uri' : ''
		}



def SignIn(redirect_uri, state):
	#Populate our runtime variables
	query_auth['state'] = state
	query_auth['redirect_uri'] = redirect_uri

	#Return the redirection endpoint with vendor-appropriate querystring
	querystring  = urllib.urlencode(query_auth)
	return endpoint_auth + '?' + querystring

def GetAccessToken(redirect_uri, code):
	#Populate our runtime variables
	query_access['code'] = code
	query_access['redirect_uri'] = redirect_uri

	#Build the URL to call with our data, ensure we use the correct header
	#to get back JSON data
	data = urllib.urlencode(query_access)
	req = urllib2.Request(endpoint_access, data, {'Accept' : 'application/json'} )

	#Call the endpoint URL and collect the response (JSON formatted)
	response = urllib2.urlopen(req)
	resp_data = json.load(response)
	
	#Extract the access token from the response
	access_token = resp_data["access_token"]
	

	#----------------------------------------------------------------
	#Build a new call, this time to the user info endpoint.
	#We'll need to pass in our shiny new access token
	querystring  = urllib.urlencode({'access_token' : access_token})
	req = urllib2.Request(endpoint_email + '?' + querystring)
	
	#Call the endpoint URL and collect the response (JSON formatted)
	response = urllib2.urlopen(req)	
	resp_data = json.load(response)

	#Extract the email address from the results
	#Accounts can have multipl emails, we're just gonna
	#Use the first
	user_email = resp_data[0]['email']
	
	return {'userEmail': user_email, 
			'accessToken' : access_token, 
			'refreshToken' : ''
			}
