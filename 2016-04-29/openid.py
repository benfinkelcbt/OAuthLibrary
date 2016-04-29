import urllib
import urllib2
import json

import jwt
import base64

provider_matrix = {
				'oic_google' :
					{
						'endpoint_auth' : 'https://accounts.google.com/o/oauth2/v2/auth',
						'endpoint_access' : 'https://www.googleapis.com/oauth2/v4/token',
						'client_id' : '635978861478-clatffch7dii7jabr9kpo7qqbhgeeqq3.apps.googleusercontent.com',
						'client_secret' : 'n6UTBM8B0WK5ycGlcghrJaar',
						'scope' : 'openid email'
					},
				'oic_yahoo' :
					{
						'endpoint_auth' : 'https://api.login.yahoo.com/oauth2/request_auth',
						'endpoint_access' : 'https://api.login.yahoo.com/oauth2/get_token',
						'client_id' : 'dj0yJmk9WDFOTTMzcVEzazBlJmQ9WVdrOVluWk5WVTlVTXpBbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD01OQ--',
						'client_secret' : '69135305896b185ccfe2cdbfda6b64059a927d6f',
						'scope' : 'openid sdpp-w'
					}					
			}

#The querystring parameters for Authorization
query_auth = {
			'response_type' : 'code', 
			'client_id' : '',
			'redirect_uri' : '',
			'scope' : '',
			'state' : ''
			}

query_access = {
		'code' : '',
		'client_id' : '',
		'client_secret' : '',
		'redirect_uri' : '',
		'grant_type' : 'authorization_code'
		}



def SignIn(provider, redirect_uri, state):
	#Populate our runtime variables
	query_auth['state'] = state
	query_auth['redirect_uri'] = redirect_uri

	#Get the appropriate endpoint and client_id for our Provider
	endpoint_auth = provider_matrix[provider]['endpoint_auth']
	query_auth['client_id'] = provider_matrix[provider]['client_id']
	query_auth['scope'] = provider_matrix[provider]['scope']

	#Return the redirection endpoint with vendor-appropriate querystring
	querystring  = urllib.urlencode(query_auth)
	return endpoint_auth + '?' + querystring

def GetAccessToken(provider, redirect_uri, code):
	#Populate our runtime variables
	query_access['code'] = code
	query_access['redirect_uri'] = redirect_uri

	endpoint_access = provider_matrix[provider]['endpoint_access']
	query_access['client_id'] = provider_matrix[provider]['client_id']
	query_access['client_secret'] = provider_matrix[provider]['client_secret']

	#Build the URL to call with our data
	data = urllib.urlencode(query_access)
	req = urllib2.Request(endpoint_access, data)

	#Call the endpoint URL and collect the response (JSON formatted)
	response = urllib2.urlopen(req)
	resp_data = json.load(response)
	
	#Extract the access token from the response
	access_token = resp_data["access_token"]
	

	#----------------------------------------------------------------
	# Pull the OpenID Connect JET token from the response data
	# This will contain our identity information


	#Get the token from the response data
	jwt_token = resp_data["id_token"]

	#split out the header and payload on the period (.) character
	#This splits it into three strings, header, payload, and signature	
	split_token = jwt_token.split('.')

	#We're interested in the payload, which is the second item 
	#Adding the three equals (===) ensures the python decoder plays nicely
	payload = base64.b64decode(split_token[1]+'===')
	payload = json.loads(payload)
	
	return {'userEmail': payload['email'], 
			'accessToken' : access_token, 
			'refreshToken' : ''
			}	