import logging
import googleOAuth

#Map the specific provider functions to provider choices
#	Additional providers must be added in here
ProviderAuthMap = {
	"google": googleOAuth.SignIn
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


def OAuthCallback(request, state):
	logging.info(request.get('state'))