"""Transaction class"""
import hashlib
from typing import List
from neon_wallet.transaction.transaction import Transaction

from neon_wallet.transaction.tx_in import TxIn
from neon_wallet.transaction.tx_out import TxOut


class BitcoinTransaction(Transaction):
    """Transaction"""

    id: str
    tx_ins: List[TxIn]
    tx_outs: List[TxOut]

    def __init__(self, tx_ins: List[TxIn], tx_outs: List[TxOut]) -> None:
        super(BitcoinTransaction, self).__init__()
        # The list of transaction entries
        self.tx_ins = tx_ins
        # The list of transaction outputs
        self.tx_outs = tx_outs
        self.id = self.get_id()

    # A method to calculate the transaction id
    # from its content
    def get_id(self) -> str:
        """get id transaction"""
        # Concatenate input ids and indices Transaction
        tx_in_content = ""
        for tx_in in self.tx_ins:
            tx_in_content += tx_in.tx_out_id + str(tx_in.tx_out_index)
        # Concatenate the addresses and amounts of the outputs of
        # the transaction
        tx_out_content = ""
        for tx_out in self.tx_outs:
            tx_out_content += tx_out.address + str(tx_out.amount)
        # Hash the content of the transaction with the SHA-256 algorithm
        tx_ou_in = tx_in_content + tx_out_content
        tx_hash = hashlib.sha256((tx_ou_in).encode()).hexdigest()
        # Return hash as transaction ID
        return tx_hash
