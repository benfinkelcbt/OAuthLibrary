import urllib
import urllib2
import json

client_id = '635978861478-clatffch7dii7jabr9kpo7qqbhgeeqq3.apps.googleusercontent.com'
client_secret = 'n6UTBM8B0WK5ycGlcghrJaar'

#The endpoints for OAuth flow
endpoint_auth = 'https://accounts.google.com/o/oauth2/v2/auth'
endpoint_access = 'https://www.googleapis.com/oauth2/v4/token'
endpoint_email = 'https://www.googleapis.com/plus/v1/people/me'

#The querystring parameters for Authorization
query_auth = {
			'response_type' : 'code', 
			'client_id' : client_id,
			'redirect_uri' : '',
			'scope' : 'email',
			'state' : ''
			}

query_access = {
		'code' : '',
		'client_id' : client_id,
		'client_secret' : client_secret,
		'redirect_uri' : '',
		'grant_type' : 'authorization_code'
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

	#Build the URL to call with our data
	data = urllib.urlencode(query_access)
	req = urllib2.Request(endpoint_access, data)

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
	user_email = resp_data['emails'][0]['value']
	
	return {'userEmail': user_email, 
			'accessToken' : access_token, 
			'refreshToken' : ''
			}
