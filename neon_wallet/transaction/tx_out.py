"""class TxOut"""


# Define a class to represent transaction output
class TxOut:
    """Tx out"""

    def __init__(self, address: str, amount: float) -> None:
        # The address of the recipient of the transaction
        self.address = address
        # The amount of the transaction in units of currency
        self.amount = amount
