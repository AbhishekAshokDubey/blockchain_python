# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 17:05:12 2018

@author: ADubey4
"""


"""Done"""
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
#from base64 import b64decode
#https://gist.github.com/lkdocs/6519366


#https://stackoverflow.com/questions/47749257/android-python-how-to-verify-signature-sha256withrsa-and-pkcs1-padding
class Crypto:
    @staticmethod
    def verify_signature(pubKey, msg, sign):
#        key = RSA.importKey(pubKey)
#        h = SHA256.new(msg)
        verifier = PKCS1_v1_5.new(pubKey)
        return verifier.verify(msg, sign)