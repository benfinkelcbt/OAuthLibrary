import logging
import googleOAuth

#Map the specific provider functions to provider choices
#	Additional providers must be added in here
ProviderAuthMap = {
	"google": googleOAuth.SignIn
}

ProviderAccessMap = {
	"google": googleOAuth.GetAccessToken
}

#--------------------------------------------------------------------------
#Call the correct sign in function based on the chosen provider
#--------------------------------------------------------------------------
def SignIn(provider, redirect_uri, state):	
	#Lookup the correct function in the tuple
	signInFunc = ProviderAuthMap.get(provider)

	#Call the function, getting the full URL + querystring in return
	authUrl = signInFunc(redirect_uri, state)
	return authUrl

#--------------------------------------------------------------------------
#Handle a callback to our applicaiton after the Grant Authorization step
#--------------------------------------------------------------------------
def OAuthCallback(request, state, provider, redirect_uri):
	#First, check for a mismatch between the State tokens and return
	#an error if found
	if (request.get('state') != state):
		return {"error" : True, "errorText" : "State Token Mismatch!  Process Aborted!"}
	
	#Next check for an error value indicating the Grant request
	#failed for some reason
	error = request.get('error')
	if (error):
		return {"error" : True, "errorText" : error}

	#No error, so continue with exchange of Authorization Code for Access and Refresh Token
	else:		
		#Lookup the correct function in the tuple
		accessFunc = ProviderAccessMap.get(provider)

		#call the function, getting our user email in the response
		userEmail = accessFunc(redirect_uri,request.get('code'))

		return {"error" : False, "errorText" : '', "userEmail" : userEmail}
