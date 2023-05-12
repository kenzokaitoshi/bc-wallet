"""class TxOut"""


class TxOut:
    """Tx out"""

    def __init__(self, address: str, amount: float) -> None:
        self.address = address
        self.amount = amount
