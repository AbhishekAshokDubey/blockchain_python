# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 21:53:28 2018

@author: ADubey4
"""


"""Done"""
#from blockchain import BlockChain
from block import Block
from tx_handler import TxHandler

class BlockHandler:
    def __init__(self, block_chain):
        self.block_chain = block_chain

    @property
    def block_chain(self):
        return self.__block_chain

    @block_chain.setter
    def block_chain(self, val):
        self.__block_chain = val
    
    def process_block(self, block):
        return self.block_chain.add_block(block) if block else False
    
    def create_block(self, addr):
        parent_block = self.block_chain.getMaxHeightBlock();
        parent_hash = parent_block.hashcode
        current_block = Block(parent_hash, addr)
        utxo_pool = self.block_chain.get_max_height_UTXOPool()
        tx_pool = self.block_chain.get_transaction_pool()
        tx_handler = TxHandler(utxo_pool)
        txs = tx_pool.getTransactions()
        r_txs = tx_handler.handle_txs(txs);
        for tx in r_txs:
            current_block.txs.append(tx)
        current_block.finalize()
        return current_block if self.block_chain.add_block(current_block) else None
    
    def process_tx(self,tx):
        self.block_chain.add_transaction(tx)