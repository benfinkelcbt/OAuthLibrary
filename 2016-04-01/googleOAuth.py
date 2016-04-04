import urllib
import urllib2
import json
import logging

client_id = '635978861478-clatffch7dii7jabr9kpo7qqbhgeeqq3.apps.googleusercontent.com'
client_secret = 'n6UTBM8B0WK5ycGlcghrJaar'

#The endpoints for OAuth flow
endpoint_auth = 'https://accounts.google.com/o/oauth2/v2/auth'
endpoint_access = 'https://www.googleapis.com/oauth2/v4/token'

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

	data = urllib.urlencode(query_access)
	req = urllib2.Request(endpoint_access, data)

	response = urllib2.urlopen(req)
	resp_data = json.load(response)
	
	logging.info(resp_data)

