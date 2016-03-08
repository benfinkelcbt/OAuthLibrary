import urllib

#The endpoints for OAuth flow
endpoint_auth = 'https://accounts.google.com/o/oauth2/v2/auth'

#The querystring parameters for Authorization
query_auth = {
			'response_type' : 'code', 
			'client_id' : '635978861478-clatffch7dii7jabr9kpo7qqbhgeeqq3.apps.googleusercontent.com',
			'redirect_uri' : '',
			'scope' : 'https://www.googleapis.com/auth/calendar.readonly',
			'state' : ''
			}


def SignIn(redirect_uri, state):
	#Populate our runtime variables
	query_auth['state'] = state
	query_auth['redirect_uri'] = redirect_uri

	#Return the redirection endpoint with vendor-appropriate querystring
	querystring  = urllib.urlencode(query_auth)
	return endpoint_auth + '?' + querystring