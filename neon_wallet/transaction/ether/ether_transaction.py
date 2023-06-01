"""ethereum transaction class"""
# Import the eth_account module to create and sign
# of ethereum transactions
from typing import Any

# import eth_account


class Transaction:
    """Define the EtherTransaction class"""

    # Define the constructor that takes the attributes as parameters
    # of an ethereum transaction
    def __init__(
        self,
        nonce: int,
        gas_price: float,
        gas_limit: int,
        to: Any,
        value: float,
        data: Any = None,
    ) -> None:
        # Assign attributes to object
        # The number of transactions already sent by the sender account
        self.nonce = nonce
        # The price of gas in wei per unit of gas
        self.gas_price = gas_price
        # The maximum amount of gas to be consumed by the transaction
        self.gas_limit = gas_limit
        # The address of the recipient account
        self.to = to
        # The amount in wei to be transferred to the recipient
        self.value = value
        # Optional data associated with the transaction
        self.data = data
