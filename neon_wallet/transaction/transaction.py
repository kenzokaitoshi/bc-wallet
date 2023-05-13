"""Transaction class"""
import hashlib
from typing import List

from neon_wallet.transaction.tx_in import TxIn
from neon_wallet.transaction.tx_out import TxOut


class Transaction:
    """Transaction"""

    id: str
    tx_ins: List[TxIn]
    tx_outs: List[TxOut]

    def __init__(self, tx_ins: List[TxIn], tx_outs: List[TxOut]) -> None:
        # The list of transaction entries
        self.tx_ins = tx_ins
        # The list of transaction outputs
        self.tx_outs = tx_outs
        self.id = self.get_id()

    # Une méthode pour calculer l'identifiant de la transaction
    # à partir de son contenu
    def get_id(self) -> str:
        """get id transaction"""
        # Concaténer les identifiants et les indices des entrées
        # de la transaction
        tx_in_content = ""
        for tx_in in self.tx_ins:
            tx_in_content += tx_in.tx_out_id + str(tx_in.tx_out_index)
        # Concaténer les adresses et les montants des sorties de
        # la transaction
        tx_out_content = ""
        for tx_out in self.tx_outs:
            tx_out_content += tx_out.address + str(tx_out.amount)
        # Hacher le contenu de la transaction avec l'algorithme SHA-256
        tx_ou_in = tx_in_content + tx_out_content
        tx_hash = hashlib.sha256((tx_ou_in).encode()).hexdigest()
        # Renvoyer le hash comme identifiant de la transaction
        return tx_hash
