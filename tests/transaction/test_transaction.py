"""test for transaction module"""
from neon_wallet.transaction.transaction import Transaction
from neon_wallet.transaction.transactions import (
    get_transaction_id,
    validate_transaction,
)
from neon_wallet.transaction.tx_in import TxIn
from neon_wallet.transaction.tx_out import TxOut
from tests.transaction.helpers_tests import utxo1, utxo2, utxo3, tx2


# Définir une méthode de test qui commence par test_
def test_get_transaction_id_valid_transaction() -> None:
    """test get transaction id valid transaction"""
    # Créer un objet transaction fictif
    _tx = Transaction(
        [
            TxIn("some previous tx id", 0, "serges007"),
            TxIn("some other previous tx id", 1, "serges007"),
        ],
        [TxOut("Alice's address", 50), TxOut("Bob's address", 100)],
    )
    # Appeler la fonction à tester avec cet objet
    tx_id = get_transaction_id(_tx)
    # Vérifier que le résultat est conforme à l'attendu
    exp = "9de05f8d7208b9c5b09518d81b73e16791afbb870e7f0273d2fc1cc2ea3c3ad0"
    assert tx_id == exp


def test_valid_transaction() -> None:
    """test valid transaction"""
    # Test that a valid transaction returns True
    a_unspent_tx_outs = [utxo1, utxo2, utxo3]
    result = validate_transaction(tx2, a_unspent_tx_outs)
    assert False is result  # True is result


def test_invalid_amount() -> None:
    """test invalid amount"""
    # Test that a transaction with a negative amount returns False
    a_unspent_tx_outs = [utxo1, utxo2, utxo3]
    tx2.tx_outs[0].amount = -5  # Modify the amount to be negative
    result = validate_transaction(tx2, a_unspent_tx_outs)
    assert False is result


def test_invalid_signature() -> None:
    """test invalid signature"""
    # Test that a transaction with an incorrect signature returns False
    a_unspent_tx_outs = [utxo1, utxo2, utxo3]
    tx2.tx_ins[0].signature = "wrong"  # Modify the signature to be wrong
    result = validate_transaction(tx2, a_unspent_tx_outs)
    assert False is result


def test_double_spend() -> None:
    """test double spend"""
    # Test that a transaction that tries to spend the same
    # UTXO twice returns False
    a_unspent_tx_outs = [utxo1, utxo2, utxo3]
    tx2.tx_ins.append(
        TxIn(tx_out_id="tx1", tx_out_index=0, signature="sig4")
    )  # Add another input that spends the same UTXO as the first input
    result = validate_transaction(tx2, a_unspent_tx_outs)
    assert False is result
