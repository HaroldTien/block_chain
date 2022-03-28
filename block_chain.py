
from hashlib import sha256
import json
import time
    

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce


    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain: 
    def __init__(self,difficulty):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.difficulty=difficulty
 
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
    @property
    def last_block(self):
        return self.chain[-1]

    
    def proof_of_work(self, block):
        block.nonce = 
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash




