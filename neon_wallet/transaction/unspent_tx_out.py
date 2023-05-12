"""class unspent transaction out"""


class UnspentTxOut:
    """unspent transaction out"""

    def __init__(
        self, tx_out_id: str, tx_out_index: int, address: str, amount: float
    ) -> None:
        self.txOutId = tx_out_id
        self.txOutIndex = tx_out_index
        self.address = address
        self.amount = amount
