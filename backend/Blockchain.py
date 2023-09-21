import hashlib
import time
import json

class ModelTransaction:
    def __init__(self, model_bytes, mean=[], std_dev=[],size=0):
        self.model_bytes = model_bytes
        self.mean = mean
        self.std_dev = std_dev
        self.size = size

    def to_dict(self):
        return {
            'model_bytes': self.model_bytes.hex(),
            'mean': self.mean.tolist(),
            'std_dev': self.std_dev.tolist(),
            'size': self.size
        }

class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        transaction_dicts = [tx.to_dict() for tx in self.transactions]
        block_data = json.dumps({
            'transactions': transaction_dicts,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
        }, sort_keys=True).encode()
        return hashlib.sha256(block_data).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block([], '0' * 64)
        self.chain.append(genesis_block)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def mine_block(self):
        last_block = self.chain[-1]
        new_block = Block(self.transactions, last_block.hash)
        self.chain.append(new_block)
        self.transactions = []

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


