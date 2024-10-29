# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2018-2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
import datetime
import hashlib


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(
            str(self.index).encode() +
            str(self.timestamp).encode() +
            str(self.data).encode() +
            str(self.previous_hash).encode()
        ).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)


def main():
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


if __name__ == '__main__':
    main()
