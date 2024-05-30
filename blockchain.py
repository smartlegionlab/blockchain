# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2018-2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
import hashlib
import json

import requests

from time import time
from urllib.parse import urlparse
from uuid import uuid4

from flask import Flask, jsonify, request


class BlockChain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        # Creating a Genesis Block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Creating a new block in the blockchain

        :param proof: <int> Evidence of work performed
        :param previous_hash: (Optional) hash of the previous block
        :return: <dict> New block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reloading the current transaction list
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Directs the new transaction to the next block

        :param sender: <str> Sender's address
        :param recipient: <str> Address of the recipient
        :param amount: <int> Sum
        :return: <int> Index of the block that will store this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block

        :param block: <dict> Block
        :return: <str>
        """

        # We need to make sure the dictionary is in order, otherwise we will have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        A simple check of the algorithm:
        - Search for the number p`, since hash(pp`) contains 4 capital zeros, where p is the previous one
        - p is the previous proof, and p` is the new one

        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Proof: Does hash(last_proof, proof) contain 4 leading zeros?

        :param last_proof: <int> Previous proof
        :param proof: <int> Current proof
        :return: <bool> True, if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self, address):
        """
        Adding a new node to the list of nodes

        :param address: <str> node address, in other words: 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Checking whether the hash included in the block is correct

        :param chain: <list> blockchain
        :return: <bool> True if it is valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check the block hash is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Checking whether the proof of work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our Consensus algorithm, it resolves conflicts,
        replacing our chain with the longest one in the chain

        :return: <bool> True if our chain had been replaced, False if not.
        """

        neighbours = self.nodes
        new_chain = None

        # We are looking only for chains longer than ours
        max_length = len(self.chain)

        # We capture and check all circuits from all network nodes
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Checking if the length is the longest and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # We replace our chain if we find another valid and longer one
        if new_chain:
            self.chain = new_chain
            return True

        return False


# Create a node instance
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Creating a Blockchain Instance
block_chain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof-of-work algorithm to get the next proof...
    last_block = block_chain.last_block
    last_proof = last_block['proof']
    proof = block_chain.proof_of_work(last_proof)

    # We should receive a reward for finding confirmation
    # Sender “0” means that the node has earned a crypto coin
    block_chain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # We create a new block by adding it to the chain
    previous_hash = block_chain.hash(last_block)
    block = block_chain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Make sure the required fields are included in the POST data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Creating a new transaction
    index = block_chain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': block_chain.chain,
        'length': len(block_chain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        block_chain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(block_chain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = block_chain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': block_chain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': block_chain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
