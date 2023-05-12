"""Transaction class"""
from typing import List

from neon_wallet.transaction.tx_in import TxIn
from neon_wallet.transaction.tx_out import TxOut


class Transaction:
    """Transaction"""

    id: str
    txIns: List[TxIn]
    txOuts: List[TxOut]
