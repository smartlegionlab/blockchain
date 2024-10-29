# Blockchain in Python

---

This project is an implementation of a blockchain in Python, 
which includes core features such as block creation, transaction processing, and a consensus algorithm. 
It consists of two modules: one implements the blockchain using Flask to create an API, 
while the other represents a simpler implementation of the blockchain using classes.

---

> Warning! This is a fairly old version that I moved to my historical repository and may continue to develop.
> So this version is still in development and research phase.

## Modules:

### 1. Flask Blockchain

This module creates a blockchain using Flask, allowing you to interact with it via HTTP requests. Key features include:

- **Creating a new block**: The `/mine` method runs the proof-of-work algorithm and creates a new block.
- **Creating a new transaction**: The `/transactions/new` method allows you to add new transactions to the blockchain.
- **Getting the full chain of blocks**: The `/chain` method returns the current chain of blocks and its length.
- **Registering new nodes**: The `/nodes/register` method allows you to add new nodes to the network.
- **Consensus algorithm**: The `/nodes/resolve` method checks and resolves conflicts in the chain of blocks.

### 2. Simple Blockchain Implementation

This module implements the basic structure of a blockchain with the `Block` and `Blockchain` classes. 
The main functions include:

- **Creating a genesis block**: The `create_genesis_block` method creates the first block in the chain.
- **Adding a new block**: The `add_block` method adds a new block to the chain, setting the correct hash of the previous block.

---

- `pip install -r requirements.txt`


- `python blockchain.py`


- `curl http://localhost:5000/mine`

```json
{
  "index": 2,
  "message": "New Block Forged",
  "previous_hash": "5d9d222c768d6c501ae28670a7333e0ae39c14d7884650bf12cf32d3961e2682",
  "proof": 35293,
  "transactions": [
    {
      "amount": 1,
      "recipient": "902a4bd96aa44abcb0d9a097bd78c462",
      "sender": "0"
    }
  ]
}

```

- `curl http://localhost:5000/mine`

```json
{
  "index": 3,
  "message": "New Block Forged",
  "previous_hash": "c67d3b156c5c3db264331196bb48efb5e6fa0fcfb31f98cf663e38d69089ffb4",
  "proof": 35089,
  "transactions": [
    {
      "amount": 1,
      "recipient": "902a4bd96aa44abcb0d9a097bd78c462",
      "sender": "0"
    }
  ]
}

```


- `curl http://localhost:5000/chain`

```json
{
  "chain": [
    {
      "index": 1,
      "previous_hash": 1,
      "proof": 100,
      "timestamp": 1730220820.929162,
      "transactions": []
    },
    {
      "index": 2,
      "previous_hash": "5d9d222c768d6c501ae28670a7333e0ae39c14d7884650bf12cf32d3961e2682",
      "proof": 35293,
      "timestamp": 1730220836.4981325,
      "transactions": [
        {
          "amount": 1,
          "recipient": "902a4bd96aa44abcb0d9a097bd78c462",
          "sender": "0"
        }
      ]
    },
    {
      "index": 3,
      "previous_hash": "c67d3b156c5c3db264331196bb48efb5e6fa0fcfb31f98cf663e38d69089ffb4",
      "proof": 35089,
      "timestamp": 1730220846.5631032,
      "transactions": [
        {
          "amount": 1,
          "recipient": "902a4bd96aa44abcb0d9a097bd78c462",
          "sender": "0"
        }
      ]
    }
  ],
  "length": 3
}

```


- `curl -X POST -H "Content-Type: application/json" -d '{
    "sender": "d4ee26eee15148ee92c6cd394edd974e",
    "recipient": "someone-other-address",
    "amount": 5
    }' "http://localhost:5000/transactions/new"`

```json
{
  "message": "Transaction will be added to Block 4"
}

```

-  `python blockchain_base.py`

```text
Index: 0
Timestamp: 2024-10-30 00:01:20.180414
Data: Genesis Block
Previous Hash: 0
Hash: 02a478085aca11b94a6ea0b5c2cfe9df56dffbe5153df269f3609faa19fc5641

Index: 1
Timestamp: 2024-10-30 00:01:20.180433
Data: Transaction Data
Previous Hash: 02a478085aca11b94a6ea0b5c2cfe9df56dffbe5153df269f3609faa19fc5641
Hash: 3a7bc11cc8e213468fc25b6708b39e41780d5673ffffb995bbfdaa909d37b73e

Index: 2
Timestamp: 2024-10-30 00:01:20.180441
Data: Another Transaction
Previous Hash: 3a7bc11cc8e213468fc25b6708b39e41780d5673ffffb995bbfdaa909d37b73e
Hash: 477333623f8b9819e23412dfda01aee127d63a2744b32515cc2d0678fcf7fac1
```

***

Author and developer: ___A.A. Suvorov.___

***

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

***

    Licensed under the terms of the BSD 3-Clause License
    (see LICENSE for details).
    Copyright © 2018-2024, A.A. Suvorov
    All rights reserved.