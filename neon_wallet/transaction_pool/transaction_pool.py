"""transaction pool module it will make it possible to manage a set of 
    transactions waiting to be included in a node of the transaction network. 
    Each node in the network has its own transaction pool, which can vary 
    depending on the node's rules and settings."""

import copy
from typing import List

from neon_wallet.transaction.transaction import Transaction


transactionPool: List[Transaction] = []


# Define function to obtain the pool of transaction
def get_transaction_pool() -> List[Transaction]:
    """get transaction pool"""
    # Return a deep copy of the transaction pool
    return copy.deepcopy(transactionPool)
