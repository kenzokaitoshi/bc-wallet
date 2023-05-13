# Importer le module unittest
import unittest
from neon_wallet.transaction.transaction import Transaction
from neon_wallet.transaction.transactions import get_transaction_id
from neon_wallet.transaction.tx_in import TxIn
from neon_wallet.transaction.tx_out import TxOut

# Importer le code à tester
import transaction


# Définir une méthode de test qui commence par test_
def test_getTransactionId_valid_transaction() -> None:
    """test get transaction id valid transaction"""
    # Créer un objet transaction fictif
    _tx = Transaction(
        [TxIn("some previous tx id", 0), TxIn("some other previous tx id", 1)],
        [TxOut("Alice's address", 50), TxOut("Bob's address", 100)],
    )
    # Appeler la fonction à tester avec cet objet
    tx_id = get_transaction_id(_tx)
    # Vérifier que le résultat est conforme à l'attendu
    assert tx_id == "some expected string"
