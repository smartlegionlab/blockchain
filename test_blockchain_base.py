# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2018-2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
import datetime

from blockchain_base import Blockchain, Block

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
