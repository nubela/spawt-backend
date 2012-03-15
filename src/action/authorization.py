#===============================================================================
# authorization library for rest api
#===============================================================================
import hashlib
import base64
import hmac

def gen_api_key(access_token, user_id):
    """
    given a auth_code, generate an api key 
    """
    key = hashlib.sha1(str(access_token))
    unsalted_key = key.hexdigest()
    unsalted_key += str(user_id)
    
    salted_key = hashlib.sha256(unsalted_key)
    return salted_key.hexdigest()

def is_api_key_validated(access_token, user_id, signature, verb, noun):
    """
    validate signature based on auth_code with a user's auth code, salting agent is usually the user's id.
    signature will be hmac and then base64 encoded.
    """
    api_key = gen_api_key(access_token, user_id)
    hmac_encrypted = base64.decodestring(signature)
    
    comparee_signature = "\n".join([verb, noun])
    comparee_hmac_encrypted = hmac.new(api_key, comparee_signature, hashlib.sha1)
    
    return comparee_hmac_encrypted.digest() == hmac_encrypted

def gen_signature(verb, noun, api_key):
    """
    generate a signature based on the supplied args
    """
    unencrypted_signature = "\n".join([verb, noun])
    hmac_encrypted = hmac.new(api_key, unencrypted_signature, hashlib.sha1)
    return base64.encodestring(hmac_encrypted.digest())

if __name__ == '__main__':
    print hmac.new("key", "nubela", hashlib.sha1).digest()