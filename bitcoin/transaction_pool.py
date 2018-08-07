# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 23:06:02 2018

@author: ADubey4
"""


"""Done"""
#from byte_array_wrapper import ByteArrayWrapper

class TransactionPool:

    def __init__(self, tx_pool = None):
        if tx_pool is None:
            self.h = {}
        else:
            self.h = tx_pool.h
    
    def add_transaction(self,tx):
#        hashcode = ByteArrayWrapper(tx.hashcode)
        hashcode = tx.hashcode
        self.h[hashcode] = tx
    
    def remove_transaction(self,tx):
#        hashcode = ByteArrayWrapper(tx.hashcode)
        hashcode = tx.hashcode
        self.h.pop(hashcode)
    
    def get_transaction(self,tx_hash):
#        hashcode = ByteArrayWrapper(tx_hash)
        hashcode = tx_hash
        return self.h.get(hashcode)
    
    def get_transactions(self):
        return list(self.h.values())