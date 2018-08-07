# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 15:15:33 2018

@author: ADubey4
"""


"""Done"""
#https://cs.stackexchange.com/questions/45287/why-does-this-particular-hashcode-function-help-decrease-collisions
#https://medium.com/@biratkirat/learning-effective-java-item-9-6b00f8eabd47
#http://garage.pimentech.net/libcommonPython_src_python_libcommon_javastringhashcode/
from Crypto.PublicKey import RSA
from utxo import *
from hashlib import sha256
#import struct


class Transaction:

    class Input:
        
        def __init__(self,prev_hash, index):
            self.prev_tx_hash = prev_hash
            self.output_index = index

        def add_signature(self,sign):
            self.signature = sign

        def equals(self,other):
            inp = other # check for pass by ref
            if ((self.prev_tx_hash != inp.prev_tx_hash) or
            (self.output_index != inp.output_index) or
            (self.signature != inp.signature)):
                return False
            return True

        def hash_code(self):
            return hash(self.prev_tx_hash + self.output_index + self.signature)
        
    class Output():
        
        def __init__(self, v, addr):
            self.value = v
            self.address = addr

        def equals(self, other):
            if (self.address.n != other.address.n) or (self.address.e != other.address.e):
                return False
            return True

        def hash_code(self):
            hashcode = 1
            hashcode = hashcode * 17 + self.value * 10000
            hashcode = hashcode * 31 + hash(self.address.e)
            hashcode = hashcode * 31 + hash(self.address.n)
            return hash(hashcode)

    def __init__(self):
        self.coinbase = False
        self.inputs = []
        self.outputs = []
        self.hashcode = b""

    @property
    def coinbase(self):
        return self.__coinbase

    @coinbase.setter
    def coinbase(self, val):
        self.__coinbase = val
        
    @property
    def hashcode(self):
        return self.__hashcode

    @hashcode.setter
    def hashcode(self, val):
        self.__hashcode = val

    @classmethod
    def from_transaction(cls,tx):
        tx_instance = cls()
        tx_instance.hashcode = tx.hashcode
        tx_instance.inputs = tx.inputs
        tx_instance.output = tx.outputs
        tx_instance.coinbase = False
        return tx_instance
        
    @classmethod
    def from_coin(cls, coin, addr):
        tx_instance = cls()
        tx_instance.coinbase = True
        tx_instance.inputs = []
        tx_instance.outputs = []
        tx_instance.add_output(coin, addr)
        tx_instance.finalize()
        return tx_instance
    
    def get_num_inputs(self):
        return len(self.inputs)
        
    def get_num_outputs(self):
        return len(self.outputs)
    
    def add_input(self, prev_tx_hashcode, output_index):
        inp = self.Input(prev_tx_hashcode, output_index)
        self.inputs.append(inp)
    
    def add_output(self, val, addr):
        op = self.Output(val, addr)
        self.outputs.append(op)
    
    def remove_input(self, val):
        if isinstance(val, int):
            self.inputs.pop(val)
        elif isinstance(val, UTXO):
            for inp in self.inputs:
                utxo = UTXO(inp.prev_tx_hash, inp.output_index)
                if (utxo.equals(u)):
                    self.inputs.remove(inp)
                    return
    
    def get_raw_data_to_sign(self,index):
        if index > len(self.inputs):
            return null
        inp = self.inputs[index]
        sign_data = b""
        prev_tx_hash = inp.prev_tx_hash
        if prev_tx_hash is not None:
            sign_data+= prev_tx_hash
        sign_data += str(inp.output_index).encode()
        for op in self.outputs:
            sign_data += str(op.value).encode()
            sign_data += str(op.address.e).encode()
            sign_data += str(op.address.n).encode()
        return sign_data
    
    def add_signature(self, sign, index):
        self.inputs[index].add_signature(sign)
    
    def get_raw_tx(self):
        raw_tx = b""
        for inp in self.inputs:
            prev_tx_hash = inp.prev_tx_hash
            if prev_tx_hash is not None:
                raw_tx += prev_tx_hash
            raw_tx += str(inp.output_index).encode()
            if signature is not None:
                raw_tx += self.inp.signature
        for op in self.outputs:
            raw_tx += str(op.value).encode()
            raw_tx += str(op.address.e).encode()
            raw_tx += str(op.address.n).encode()
        return raw_tx

    def finalize(self):
        try:
            self.hashcode = sha256(self.get_raw_tx()).digest()
        except Exception as e:
            print(e)
            raise Exception("Error Hashing the Trancation")
    
    def equals(self,other_tnx = None):
        if other_tnx is None:
            return False
        if (self.get_num_inputs() != other_tnx.get_num_inputs) or (self.get_num_outputs() != other_tnx.get_num_outputs):
            return False
        for i, inp in enumerate(other_tnx.inputs):
            if not self.inputs[i].equals(inp):
                return False
        for i, op in enumerate(other_tnx.outputs):
            if not self.outputs[i].equals(op):
                return False
        return True
    
    def generate_hashcode():
        hashcode = 1
        for inp in self.inputs:
            hashcode += 31*inp.hash_code()
        for op in self.outputs:
            hashcode += 31*op.hash_code()
        return hashcode