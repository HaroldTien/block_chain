
import hashlib
from operator import ne
from os import get_handle_inheritable
import time

class Transaction:
    def __init__(self,sender,receiver,amounts,fee,message):
        self.sender=sender
        self.receiver=receiver
        self.amounts=amounts
        self.fee=fee
        self.message=message

class Block:
    def __init__(self,previous_hash,difficulty,miner,miner_rewards) -> None:
        self.previous_hash=previous_hash
        self.hash=''
        self.difficulty=difficulty
        self.nonce=0
        self.timestamp=int(time.time())
        self.transactions=[]
        self.miner=miner
        self.miner_rewards=miner_rewards

class Block_chain:
    def __init__(self) -> None:
        self.adjust_difficulty_blocks=10
        self.difficulty=1
        self.block_time=30
        self.miner_reward=10
        self.block_limitation=32
        self.chain=[]
        self.pending_transactions=[]

    #-----> These functions for get hash value
    def transaction_to_string(self,transaction):
        transaction_dict={
            'sender':str(transaction.sender),
            'receiver':str(transaction.receiver),
            'amounts':str(transaction.amounts),
            'fee':str(transaction.fee),
            'message':str(transaction.message),
        }
        return transaction_dict

    def get_transactions_string(self,block):
        transaction_str=''
        for transaction in block.transactions:
            transaction_str+=self.transaction_to_string(transaction)
        return transaction_str

    def get_hash(self,block,nonce):
        s=hashlib.sha1()
        s.update(
            block.previous_hash+
            str(block.timestamp)+
            self.get_transactions_string(block)+
            str(nonce)
        ).encode('utf-8')
        h=s.hexdigest()
        return h
    #------<

    def create_genesis_block(self):
        print('Creating genesis block...')
        new_block=Block('Hello world',self.difficulty,'Harold',self.miner_reward)
        new_block.hash=self.get_hash(new_block,0)
        self.chain.append(new_block)
    
    # def add_transaction_to_block(self,block): #originally
    #     self.pending_transactions.sort(key=lambda x: x.fee,reverse=True)
    #     if len(self.pending_transactions) > self.block_limitation:
    #         transaction_accepted=self.pending_transactions[:self.block_limitation]
    #         self.pending_transactions=self.pending_transactions[self.block_limitation:]
    #     else:
    #         transaction_accepted=self.pending_transactions
    #         self.pending_transactions=[]
    #         block.transactions=transaction_accepted

    def add_transaction_to_block(self,block): #alter
        self.pending_transactions.sort(key=lambda x: x.fee,reverse=True)
        if(len(self.pending_transactions>self.block_limitation)):
            block.transactions.append(self.pending_transactions[:self.block_limitation])
            self.pending_transactions=self.pending_transactions[self.block_limitation:]
        else:
            block.transactions.append(self.pending_transactions)
            self.pending_transactions=[]
    
        
    def mine_block(self,miner):
        start_time=time.process_time()
        last_block=self.chain[-1]
        new_block=Block(last_block.hash,self.difficulty,miner,self.miner_reward)
        self.add_transaction_to_block(new_block)
        new_block.previous_hash=last_block.hash
        new_block.hash=self.get_hash(new_block,new_block.nonce)

        #--->  make sure th amount of zero in front of nonce are match the that of difficulty
        while(new_block.hash[0:self.difficulty]!='0'*self.difficulty):
            new_block.nonce+=1 
            new_block.hash=self.get_hash(new_block,new_block.nonce)
        #<----
        time_consumed=round(time.process_time-start_time,5)
        
        print('hash found: ',new_block.hash,'\n','difficulty: ',new_block.difficulty,'\n','time consumed: ',time_consumed)
        
        self.chain.append(new_block)




