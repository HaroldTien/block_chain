from ctypes import resize
import hashlib
import time
import rsa

class Transaction:
    def __init__(self,sender,receiver,amounts,fee,message):
        self.sender=sender
        self.receiver=receiver
        self.amounts=amounts
        self.fee=fee
        self.message=message

class Block:
    def __init__(self,previous_hash,difficulty,miner,miner_rewards):
        self.previous_hash=previous_hash
        self.hash=''
        self.difficulty=difficulty
        self.nonce=0
        self.timestamp=int(time.time())
        self.transactions=[]
        self.miner=miner
        self.miner_rewards=miner_rewards


class Block_chain:
    def __init__(self):
        self.adjust_difficulty_blocks=10
        self.difficulty=1
        self.block_time=30
        self.miner_rewards=10
        self.block_limitation=32
        self.chain=[]
        self.pending_transactions=[]

    def transaction_to_string(self,transaction):
        transaction_dict={
            'snder':str(transaction.sender),
            'receiver':str(transaction.receiver),
            'amounts':transaction.amounts,
            'fee':transaction.fee,
            'message':transaction.message
        }
        return str(transaction_dict)

    def get_transactions_string(self,block):
        transaction_str=''
        for transaction in block.transactions:
            transaction_str+=self.transaction_to_string(transaction)
        return transaction_str

    def get_hash(self,block,nonce):
        s=hashlib.sha1()
        s.update(
            (block.previous_hash+
            str(block.timestamp)+
            self.get_transactions_string(block)+
            str(nonce)
            ).encode('utf-8')
        )
        h=s.hexdigest()
        return h


    #create a genesis block
    def create_genese_block(self):
        print('create genesis block....')
        new_block=Block('Hello ward',self.difficulty,'Harold',self.miner_rewards)
        new_block.hash=self.get_hash(new_block,0)
        self.chain.append(new_block)

    #add the transaction to block
    def add_tarnsaction_to_blocks(self,block):
        self.pending_transactions.sort(key=lambda x: x.fee,reverse=True)
        if len(self.pending_transactions)>self.block_limitation:
            transction_accepted=self.pending_transactions[:self.block_limitation]
            self.pending_transactions=self.pending_transactionsp[self.block_limitation:]
        else:
            transction_accepted=self.pending_transactions
            self.pending_transactions=[]
            block.transactions=transction_accepted

    def mine_block(self,miner):
        start=time.process_time()
        last_block=self.chain[-1]
        new_block=Block(last_block.hash,self.difficulty,miner,self.miner_rewards)

        self.add_tarnsaction_to_blocks(new_block)
        new_block.previous_hash=last_block.hash
        new_block.difficulty=self.difficulty
        new_block.hash=self.get_hash(new_block,new_block.nonce)

        while new_block.hash[0:self.difficulty] != '0'*self.difficulty:
            new_block.nonce+=1
            new_block.hash=self.get_hash(new_block,new_block.nonce)
        
        time_consumed=round(time.process_time()-start,5)
        print(f"Hash found:{new_block.hash}@difficulty{self.difficulty},time cost: {time_consumed}s")
        self.chain.append(new_block)

    def adjust_difficulty(self):
        if len(self.chain)%self.adjust_difficulty_blocks != 1:
            return self.difficulty
        elif len(self.chain)<=self.adjust_difficulty_block:
            return self.difficulty
        else:
            start=self.chain[-1* self.adjust_difficulty_blocks-1].timestamp
            finish=self.chain[-1].timestamp
            average_time_consumed=round((finish-start)/(self.adjust_difficulty_blocks),2)
            if average_time_consumed>self.block_time:
                print(f"Average block time:{average_time_consumed}s. Lower the difficulty")
                self.difficulty-=1
            else:
                print(f"Average block time:{average_time_consumed}.s High up the difficulty")
                self.difficulty+=1

    def get_balance(self,account):
        balance=0
        for block in self.chain:
            #check miner reward
            miner=False
            if block.miner==account:
                miner==True
                balance+=transaction.miner_rewards
            for transaction in block.transaction:
                if miner:
                    balance+=transaction.fee
                if transaction.sender==account:
                    balance-=transaction.amounts
                    balance-=transaction.fee
                elif transaction.receiver==account:
                    balance+=transaction.amounts
        return balance

    def verify_blockchain(self):
        previous_hash=''
        for idx,block in enumerate(self.chain):
            # print(idx,':',block,'\n')
            if self.get_hash(block,block.nonce)!= block.hash:
                print("Error:Hash not matched!")
                return False
            elif previous_hash!= block.previous_hash and idx:
                print('Error:Hash not matched to previous_hash')
                return False
        previous_hash=block.hash
        print('Hash correct!')
        return True

    def generate_address(self):
        public,private=rsa.newkeys(512)
        public_key=public.save_pkcs1()
        private_key=private.save_pkcs1()
        return self.get_address_from_public(public_key),private_key

    def get_address_from_public(self,public):
        address=str(public).replace('\\n','')
        address=address.replace("b'-----BEGIN RSA PUBLIC KEY-----",'')
        address=address.replace("-----END RSA PUBLIC KEY-----'",'')
        address=address.replace(' ','')
        print('address:',address)
    
    def initialize_transaction(self,sender,receiver,amount,fee,message):
        if self.get_balance(sender)<amount+fee:
            print('Balance not enough!')
            return False
        new_transaction=Transaction(sender,receiver,amount,fee,message)
        return new_transaction

    def sign_transaction(self,transaction,private_key):
        private_key_pkcs=rsa.PublicKey.load_pkcs1(private_key)
        transaction_str=self.get_transactions_string(transaction)
        signature=rsa.sign(transaction_str.encode('utf-8'),private_key_pkcs,'SHA-1')
        return signature


    def add_transaction(self,transaction,signature):
        public_key='-----BEGIN RSA PUBLIC KEY-----\n'
        public_key+=transaction.sender
        public_key+='\n-----END RSA PUBLIC KEY-----\n'
        public_key_pkcs=rsa.PublicKey.load_pkcs1(public_key.encode('utf-8'))
        transaction_str=self.transaction_to_string(transaction)
        if transaction.fee+transaction.amount>self.get_balance(transaction.sender):
            print('Balance not enough!')
            return False
        try:
            rsa.verify(transaction_str.encode('utf-8'),signature,public_key_pkcs)
            print("Authorized successfully!")
            self.pending_transactions.append(transaction)
            return True
        except Exception:
            print("RSA Verified wrong")

        

if __name__=='__main__':
    block_chain=Block_chain()

    


    


