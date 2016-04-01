#Encryption libraries
import datetime
import hmac
import hashlib
import base64

def generate_state_parameter(private_key):
	#Uses a private key and the current datetime to produce a URL-Safe
	#state parameter to prevent CSRF
    
	#A datetime parameter, essentially a random seed
    date = datetime.datetime.today()
    
    #Create a hash from our private key and random seed (current datetime) using sha1 encryption
    raw_state = str(date)
    hashed = hmac.new(private_key, raw_state, hashlib.sha1) 

    #Base64 encode the binary hash so it can be used in a querystring
    state = base64.b64encode(hashed.digest())
    return {'state':state, 'date': date}