"""class TxIn"""


# Define a class to represent a transaction input
class TxIn:
    """Transaction in class"""

    def __init__(
        self,
        tx_out_id: str,
        tx_out_index: int,
        signature: str,
    ) -> None:
        # The identifier of the transaction output to
        # which this entry refers to
        self.tx_out_id = tx_out_id
        # The transaction output index
        # to which this entry refers
        self.tx_out_index = tx_out_index
        self.signature = signature
