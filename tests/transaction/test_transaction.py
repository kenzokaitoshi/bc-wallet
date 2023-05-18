"""test for transaction module"""
from neon_wallet.transaction.transaction import Transaction
from neon_wallet.transaction.transactions import (
    find_unspent_tx_out,
    get_transaction_id,
    get_tx_in_amount,
    has_duplicates,
    is_valid_address,
    is_valid_transaction_structure,
    is_valid_tx_in_structure,
    is_valid_tx_out_structure,
    validate_transaction,
    validate_tx_in,
)
from neon_wallet.transaction.tx_in import TxIn
from neon_wallet.transaction.tx_out import TxOut
from neon_wallet.transaction.unspent_tx_out import UnspentTxOut
from tests.transaction.helpers_tests import (
    seeder,
    utxo1,
    utxo2,
    utxo3,
    tx2,
    address,
    private_key,
)
from tests.helpers_data import tx_out_address


# Define a test method that starts with test_
def test_get_transaction_id_valid_transaction() -> None:
    """test get transaction id valid transaction"""
    # Create a dummy transaction object
    _tx = Transaction(
        [
            TxIn("some previous tx id", 0, "serges007"),
            TxIn("some other previous tx id", 1, "serges007"),
        ],
        [TxOut("Alice's address", 50), TxOut("Bob's address", 100)],
    )
    # Call the function to test with this object
    tx_id = get_transaction_id(_tx)
    # Check that the result is as expected
    exp = "073365f8863b5c837acd55a5e6ffbcce07d955bb0354fa2c58f5827f26f3dfdf"
    assert tx_id == exp


def test_validate_tx_in() -> None:
    """test valid transaction in"""
    # Create an unspent exit belonging to this address
    # with an arbitrary amount
    unspent_tx_out = UnspentTxOut("1234", 0, address, 100)

    # Create a list containing this unspent output
    a_unspent_tx_outs = [unspent_tx_out]

    # Create a transaction input that references this unspent output
    # Create a transaction input that references this unspent output
    tx_in = TxIn("1234", 0, "")

    # Create a new transaction that contains this transaction entry
    # and an arbitrary transaction output
    transaction = Transaction([tx_in], [TxOut("abcd", 50)])

    # Sign the transaction entry with the private key and id of
    # the transaction
    tx_in.signature = private_key.sign(bytes.fromhex(transaction.id)).hex()

    # Test the validate_tx_in function with this data
    result = validate_tx_in(tx_in, transaction, a_unspent_tx_outs)

    assert True is result


def test_valid_transaction() -> None:
    """test valid transaction"""
    # Create an unspent exit belonging to this address
    # with an arbitrary amount
    unspent_tx_out = UnspentTxOut("1234", 0, address, 50)

    # Create a list containing this unspent output
    a_unspent_tx_outs = [unspent_tx_out]

    # Create a transaction input that references this unspent output
    # Create a transaction input that references this unspent output
    tx_in = TxIn("1234", 0, "")

    # Create a new transaction that contains this transaction entry
    # and an arbitrary transaction output
    tx_2 = Transaction(
        [tx_in],
        [
            TxOut(
                tx_out_address,
                50,
            )
        ],
    )

    # Sign the transaction entry with the private key and id of
    # the transaction
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


def test_is_valid_transaction_structure() -> None:
    """test is valid transaction structure"""
    tansaction = seeder()[0]
    assert True is is_valid_transaction_structure(tansaction)


def test_invalid_transaction_structure() -> None:
    """test invalid transaction structure"""
    assert False is is_valid_transaction_structure(tx2)


def test_is_valid_tx_in_structure() -> None:
    """test is_valid_tx_in_structure function"""
    tx_in = seeder()[2]
    assert True is is_valid_tx_in_structure(tx_in)


def test_invalid_tx_in_structure() -> None:
    """test is invalid_tx_in_structure function"""
    tx_in = TxIn(
        tx_out_id="tx1",
        tx_out_index="0",
        signature="sig",
    )
    assert False is is_valid_tx_in_structure(tx_in)


def test_is_valid_tx_out_structure() -> None:
    """test is_valid_tx_out_structure function"""
    tx_out = TxOut(
        tx_out_address,
        50,
    )
    assert True is is_valid_tx_out_structure(tx_out)


def test_is_valid_address() -> None:
    """test is_valid_address function"""
    assert True is is_valid_address(tx_out_address)


def test_is_invalid_address() -> None:
    """test is_valid_address function"""
    _address = "99f998e8e8ce23f37cb9d60c73f10fe4"
    assert False is is_valid_address(_address)


def test_get_tx_in_amount() -> None:
    """test_get_tx_in_amount function"""
    _tx, a_unspent_tx_outs, tx_in = seeder()
    assert get_tx_in_amount(tx_in, a_unspent_tx_outs) == 50


def test_find_unspent_tx_out() -> None:
    """test find_unspent_tx_out"""
    _tx, a_unspent_tx_outs, tx_in = seeder()
    assert (
        find_unspent_tx_out(
            _tx.id,
            tx_in.tx_out_index,
            a_unspent_tx_outs,
        )
        is None
    )


def test_has_duplicates() -> None:
    """test if Txins has duplicates values"""
    assert True is has_duplicates(tx2.tx_ins)


def test_has_not_duplicates() -> None:
    """test if Txins has not duplicates values"""
    tx_ins = seeder()[2]
    assert False is has_duplicates([tx_ins])
