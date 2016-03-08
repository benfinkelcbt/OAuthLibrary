#Basic imports
import datetime

#OAuth utilities
import utilities


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


def SignIn(redirect_uri):
	
	#Generate our state variable
	stateObj = utilities.generate_state_parameter(query_auth['client_id'], '12345')

	#Populate our runtime variables
	query_auth['state'] = stateObj['state']		
	query_auth['redirect_uri'] = redirect_uri

	#Hand the state back to the calling application so validation can be performed
	return(stateObj)

