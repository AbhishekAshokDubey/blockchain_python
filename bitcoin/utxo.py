# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 15:44:15 2018

@author: ADubey4
"""


"""Done"""
# http://gerg.ca/blog/post/2012/python-comparison/
# https://docs.python.org/3.5/library/functools.html#functools.total_ordering
from functools import total_ordering
import copy

@total_ordering
class UTXO :

    @staticmethod
    def cmp(a, b):
        return (a > b) - (a < b)
    
    def __init__(self, tx_hash, index):
        self.tx_hash = copy.copy(tx_hash)
        self.index = index
    
    def equals(self, other_utxo=None):
        return ((self.tx_hash == other_utxo.tx_hash) and (self.index == other_utxo.index))
    
    def get_hash_code(self):
        hash_code = 1
        hash_code = 17 + self.index
        hash_code = hash_code * 31 + hash(self.tx_hash) 
        return hash_code
    
    ## everything below: the way to implemet a comparable in python
    def __cmp__(self, other_utxo):
        other_hashcode = other_utxo.tx_hash
        other_index = other_utxo.index
        if(other_index > self.index):
            return -1
        elif (other_index < self.index):
            return 1
        else:
            if len(other_hashcode) > len(self.tx_hash):
                return -1
            elif len(other_hashcode) < len(self.tx_hash):
                return 1
            else:
                return self.cmp(self.tx_hash, other_hashcode)

    # __cmp__ is removed from python 3.X and hence we need to implemet something move
    def __eq__(self, other):
        return self.__cmp__(other) == 0
    def __lt__(self, other):
        return self.__cmp__(other) < 0

    # required only when we use the object as dict key or in set
    # as they Data structures uses hash internally
#    def __hash__(self):
#        return self.get_hash_code()    

# below code is not required because of @total_ordering, else we would need everything below
#    def __ne__(self, other):
#        return self.__cmp__(other) != 0
#    def __gt__(self, other):
#        return self.__cmp__(other) > 0
#    def __ge__(self, other):
#        return self.__cmp__(other) >= 0
#    def __le__(self, other):
#        return self.__cmp__(other) <= 0