"""test for transaction module"""
from neon_wallet.transaction.transaction import Transaction
from neon_wallet.transaction.transactions import (
    get_transaction_id,
    validate_transaction,
    validate_tx_in,
)
from neon_wallet.transaction.tx_in import TxIn
from neon_wallet.transaction.tx_out import TxOut
from neon_wallet.transaction.unspent_tx_out import UnspentTxOut
from tests.transaction.helpers_tests import (
    utxo1,
    utxo2,
    utxo3,
    tx2,
    address,
    private_key,
)


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
    exp = "073365f8863b5c837acd55a5e6ffbcce07d955bb0354fa2c58f5827f26f3dfdf"
    assert tx_id == exp


def test_validate_tx_in() -> None:
    """test valid transaction in"""
    # Créer une sortie non dépensée appartenant à cette adresse
    # avec un montant arbitraire
    unspent_tx_out = UnspentTxOut("1234", 0, address, 100)

    # Créer une liste contenant cette sortie non dépensée
    a_unspent_tx_outs = [unspent_tx_out]

    # Créer une entrée de transaction qui référence cette sortie non dépensée
    # Créer une entrée de transaction qui référence cette sortie non dépensée
    tx_in = TxIn("1234", 0, "")

    # Créer une nouvelle transaction qui contient cette entrée de transaction
    # et une sortie de transaction arbitraire
    transaction = Transaction([tx_in], [TxOut("abcd", 50)])

    # Signer l'entrée de transaction avec la clé privée et l'identifiant de
    # la transaction
    tx_in.signature = private_key.sign(bytes.fromhex(transaction.id)).hex()

    # Tester la fonction validate_tx_in avec ces données
    result = validate_tx_in(tx_in, transaction, a_unspent_tx_outs)

    # Afficher le résultat
    assert True is result


def test_valid_transaction() -> None:
    """test valid transaction"""
    # Créer une sortie non dépensée appartenant à cette adresse
    # avec un montant arbitraire
    unspent_tx_out = UnspentTxOut("1234", 0, address, 50)

    # Créer une liste contenant cette sortie non dépensée
    a_unspent_tx_outs = [unspent_tx_out]

    # Créer une entrée de transaction qui référence cette sortie non dépensée
    # Créer une entrée de transaction qui référence cette sortie non dépensée
    tx_in = TxIn("1234", 0, "")

    # Créer une nouvelle transaction qui contient cette entrée de transaction
    # et une sortie de transaction arbitraire
    tx_2 = Transaction(
        [tx_in],
        [
            TxOut(
                "04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a",
                50,
            )
        ],
    )

    # Signer l'entrée de transaction avec la clé privée et l'identifiant de
    # la transaction
    tx_in.signature = private_key.sign(bytes.fromhex(tx_2.id)).hex()

    result = validate_transaction(tx_2, a_unspent_tx_outs)
    assert True is result


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
