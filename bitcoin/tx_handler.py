# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 23:52:12 2018

@author: ADubey4
"""


"""Done"""
# https://stackoverflow.com/questions/3718383/why-should-a-java-class-implement-comparable

from utxo import UTXO
from crypto import Crypto
from utxo_pool import UTXOPool
from transaction import Transaction


class TxHandler:
    def __init__(self, utxo_pool):
        self.utxo_pool = UTXOPool(utxo_pool)


    """
     * @return true if:
     * (1) all outputs claimed (consumed from previous transactions) by {@code tx} are in the current UTXO pool,
     * (2) the signatures on each input of {@code tx} are valid,
     * (3) no UTXO is claimed multiple times by {@code tx},
     * (4) all of {@code tx}s output values are non-negative, and
     * (5) the sum of {@code tx}s input values is greater than or equal to the sum of its output
     * values; and false otherwise.
     * @code tx is the current transaction
     """        
    def isValidTx(self,tx:Transaction):
        utxo_used_this_tx = []
        input_sum = 0
        output_sum = 0

        for i, inp in enumerate(tx.inputs):
            utxo = UTXO(inp.prev_tx_hash, inp.output_index)
            # (1)
            if not self.utxo_pool.contains(utxo):
                return False
            
            # (2)
            previous_tx_output_corresponding_to_inp = self.utxo_pool.get_transaction_output(utxo)
            public_key = previous_tx_output_corresponding_to_inp.address;
            raw_tx_message = tx.get_raw_data_to_sign(i);
            if not Crypto.verify_signature(public_key, raw_tx_message, inp.signature):
                return False
            
            # (3)
            if utxo in utxo_used_this_tx:
                return False
            
            utxo_used_this_tx.append(utxo)
            input_sum += previous_tx_output_corresponding_to_inp.value;
        
        # (4)
        for op in tx.outputs:
            if op.value < 0: return False
            output_sum += op.value
        
        # (5)
        return (input_sum >= output_sum)
        
        
    def handle_txs(self,possible_txs):
        valid_tx = []
        for tx in possible_txs:
            if not self.isValidTx(tx):
                continue
            
            valid_tx.append(tx)
            for inp in tx.inputs:
                used_utxo = UTXO(inp.prev_tx_hash, inp.output_index)
                self.utxo_pool.remove_utxo(used_utxo)

            tx_hashcode = tx.hashcode # should this refresh ?
            for i, op in enumerate(tx.outputs):
                new_utxo = UTXO(tx_hashcode, i)
                self.utxo_pool.add_utxo(new_utxo,op)
        
        return valid_tx
    
    def get_utxo_pool(self):
        return self.utxo_pool