import datetime

from blockchain import Blockchain, Block

my_blockchain = Blockchain()
my_blockchain.add_block(Block(1, datetime.datetime.now(), "Transaction Data", ""))
my_blockchain.add_block(Block(2, datetime.datetime.now(), "Another Transaction", ""))

for block in my_blockchain.chain:
    print("Index:", block.index)
    print("Timestamp:", block.timestamp)
    print("Data:", block.data)
    print("Previous Hash:", block.previous_hash)
    print("Hash:", block.hash)
    print()
