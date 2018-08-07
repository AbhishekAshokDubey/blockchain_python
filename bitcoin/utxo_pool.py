# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 01:33:52 2018

@author: ADubey4
"""


"""Done"""
import copy

class UTXOPool:
    def __init__(self, utxo_pool=None):
        if utxo_pool is None:
            self.H = {}
        else:
            self.H = copy.deepcopy(utxo_pool)
    
    def add_utxo(self, utxo, tx_op):
        self.H[utxo] = tx_op
    
    def remove_utxo(self,utxo):
        self.pop(utxo)
    
    def get_transaction_output(self, utxo):
        return self.H.get(utxo)
    
    # this is why we need comparable UTXO
    def contains(self, utxo):
        return utxo in self.h.keys()
    
    def get_all_utxo(self):
        return list(self.h.keys())