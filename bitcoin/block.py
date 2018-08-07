# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 17:18:24 2018
@author: ADubey4
"""


"""Done"""
from transaction import Transaction
from hashlib import sha256
#https://stackoverflow.com/questions/68645/are-static-class-variables-possible
class Block:
    # Static variable
    COINBASE = 25

    def __init__(self, prev_block_hash, addr):
        self.hashcode = b""
        self.prev_block_hash = prev_block_hash
        self.coinbase = Transaction.from_coin(Block.COINBASE, addr)
        self.txs = [];
    
    def get_raw_block(self):
        raw_block = b""
        if self.prev_block_hash is not None:
            raw_block += self.prev_block_hash
        for tnx in self.txs:
            raw_block += tnx.get_raw_tx()
        return raw_block
    
    def add_transaction(self, tx):
        self.txs.append(tx)
    
    def finalize(self):
        try:
            self.hashcode = sha256(self.get_raw_block()).digest()
        except Exception as e:
            print(e)
            raise Exception("Error Hashing the block")