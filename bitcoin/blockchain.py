# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 17:47:33 2018

@author: ADubey4
"""


""" Done """
#from collections import defaultdict
from utxo_pool import UTXOPool
#from byte_array_wrapper import ByteArrayWrapper
from transaction_pool import TransactionPool
from tx_handler import TxHandler
from utxo import UTXO

class BlockChain:
    CUT_OFF_AGE = 10;
    class BlockPlus:
        def __init__(self, block, index, utxo_pool):
            self.block = block
            self.index = index
            self.utxo_pool = utxo_pool

        @property
        def utxo_pool(self):
            return self.__utxo_pool
    
        @utxo_pool.setter
        def utxo_pool(self, val):
            self.__utxo_pool = val
        
        def get_utxo_pool_copy(self):
            return UTXOPool(self.utxo_pool)
    
    def __init__(self,genesis_block):
        utxo_pool = UTXOPool();
        self.tx_pool = TransactionPool();
        block_plus_to_add = self.BlockPlus(genesis_block, 1, utxo_pool);
#        hash_content_byte_wrapper = ByteArrayWrapper(genesis_block.hash);
        hash_content = genesis_block.hash;
        self.block_chain = {}
        self.block_chain[hash_content] = block_plus_to_add;
        self.last_block_plus = block_plus_to_add;
        # if the first guy gets the coinbase 
        self.add_coinbase_to_UTXOPool(genesis_block, utxo_pool);
    
    def get_max_height_block(self):
        return self.last_block_plus.block
    
    def get_max_height_UTXOPool(self):
        return self.last_block_plus.get_utxo_pool_copy()
    
    def get_transaction_pool(self):
        return self.tx_pool
    
    def add_block(self, block):
        
        # check for parent block hash
        prev_block_hash = block.prev_block_hash
        if prev_block_hash is None:
            return False

        # check for parent block
#        parent_block_plus = self.block_chain.get(ByteArrayWrapper(prev_block_hash))
        parent_block_plus = self.block_chain.get(prev_block_hash)
        if parent_block_plus is None:
            return False

        # validate transactions in current block wrt to its parent block's utxoPool (unspent at parents time can only be spent this time)
        tx_handler = TxHandler(parent_block_plus.get_utxo_pool_copy());
        current_txs = block.txs;

        # check all the currentTxs are valid
        # Note: handleTxs() also updates the corresponding utxoPool
        valid_txs = tx_handler.handle_txs(current_txs)
        if len(current_txs) != len(valid_txs):
            return False
        
        # Looks all good, we can add the block now if it has not reached the cut_off
        # should not be older than CUT_OFF_AGE from last_block_plus
        if (parent_block_plus.index + 1 <= self.last_block_plus.index - BlockChain.CUT_OFF_AGE):
            return False
        
        utxo_pool = tx_handler.get_utxo_pool()
        # update utxo_pool for coinbase tx
        self.add_coinbase_to_utxo_pool(block, utxo_pool)
        block_plus_to_add = self.BlockPlus(block, parent_block_plus.index + 1, utxo_pool);
#        self.block_chain[ByteArrayWrapper(block.hashcode)] = block_plus_to_add
        self.block_chain[block.hashcode] = block_plus_to_add
        if parent_block_plus.index + 1 > self.last_block_plus.index:
            self.last_block_plus = block_plus_to_add
        return True
    
    def add_coinbase_to_utxo_pool(self, block, utxo_pool):
        tx = block.coinbase
        for i, op in enumerate(tx.outputs):
            utxo = UTXO(tx.hashcode, i)
            utxo_pool.append(utxo, op)
    
    def add_transaction(self,tx):
        self.tx_pool.add_transaction(tx)