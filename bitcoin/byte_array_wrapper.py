# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 23:00:07 2018

@author: ADubey4
"""

"""Done"""

class ByteArrayWrapper:
    def __init__(self, b):
        self.contents = b
    
    def equals (self, other_baw):
        return self.contents == other_baw
    
    def hash_code(self):
        return hash(self.contents)