"""unitest test of bitcoin wallet module"""
from typing import List
from neon_wallet.transaction.coins.unspent_tx_out import UnspentTxOut
from neon_wallet.wallet.core import wallet
from tests.transaction.helpers_tests import unspent_tx_outs_of_address
from tests.helpers_data import private_key


wallet_ = wallet("BTC")


def test_check_symbol() -> None:
    """test check if symbol correspond to the wallet"""
    assert wallet_.symbol == "BTC"


def test_get_private_from_wallet() -> None:
    """test get private key of current wallet"""
    assert True is isinstance(wallet_.private_key, str)
    assert len(wallet_.private_key) == 64


def test_get_public_from_wallet() -> None:
    """test get private key of current wallet"""
    assert True is isinstance(wallet_.public_key, str)
    assert len(wallet_.public_key) == 130


def test_get_account_balance() -> None:
    """test get wallet balance"""
    addrx = wallet_.get_address()
    utxo = unspent_tx_outs_of_address(addrx)
    balance = wallet_.get_balance(addrx, utxo)
    assert balance == 50


def test_get_address() -> None:
    """test get address of wallet"""
    _w = wallet("BTC")
    _w.private_key = private_key
    assert True is isinstance(_w.get_address(), str)
    assert len(_w.get_address()) == 34


def test_set_unspent_tx_outs() -> None:
    """test get and set method of unspent transaction outs of wallet"""
    wallet_1 = wallet("BTC")
    addrx = wallet_1.get_public_from_wallet()
    utxo = unspent_tx_outs_of_address(addrx)
    wallet_1.set_unspent_tx_outs(utxo)
    assert True is isinstance(wallet_1.unspent_tx_outs, List)
    utxos = wallet_1.get_unspent_tx_outs()
    assert len(utxos) == 1
    assert True is all(isinstance(utxo, UnspentTxOut) for utxo in utxos)


def test_get_my_unspent_transaction_outputs() -> None:
    """test get address of wallet"""
    wallet_1 = wallet("BTC")
    addrx = wallet_1.get_public_from_wallet()
    utxo = unspent_tx_outs_of_address(addrx)
    wallet_1.set_unspent_tx_outs(utxo)
    outputs = wallet_1.get_my_unspent_transaction_outputs()
    print("test here")
    assert True is isinstance(outputs, list)
    assert True is all(isinstance(output, UnspentTxOut) for output in outputs)
    assert True is all(
        True
        if (
            output.tx_out_id == "1234"
            and output.tx_out_index == 0
            and output.address == addrx
            and output.amount == 50
        )
        else False
        for output in outputs
    )


def test_get_unspent_tx_outs() -> None:
    """test set unspent tx outs"""
    # Create a wallet with the symbol "BTC"
    alice = wallet("BTC")
    benjamin = wallet("BTC")
    steve = wallet("BTC")

    # Create some unspent outputs with dummy values
    unspent_tx_outs = [
        UnspentTxOut("tx1", 0, alice.get_public_from_wallet(), 10),
        UnspentTxOut("tx2", 1, benjamin.get_public_from_wallet(), 20),
        UnspentTxOut("tx3", 2, steve.get_public_from_wallet(), 30),
    ]
    # Set the wallet's unspent outputs to the list
    alice.set_unspent_tx_outs(unspent_tx_outs)
    utxos = alice.get_unspent_tx_outs()
    assert len(utxos) == 3
    assert True is all(isinstance(utxo, UnspentTxOut) for utxo in utxos)


def test_send_transaction() -> None:
    """test get unspent tx outs"""
    alice = wallet("BTC")
    benjamin = wallet("BTC")
    unspent_tx_outs = [
        UnspentTxOut("tx1", 0, alice.get_public_from_wallet(), 10),
        UnspentTxOut("tx2", 1, alice.get_public_from_wallet(), 20),
        UnspentTxOut("tx2", 2, benjamin.get_public_from_wallet(), 30),
    ]
    alice.set_unspent_tx_outs(unspent_tx_outs)
    alice.send_transaction(benjamin.get_public_from_wallet(), 10)


# def send_transaction(self, address: str, amount: float)
# def find_unspent_tx_outs
# def find_tx_outs_for_amount
# def create_tx_outs
# def filter_tx_pool_txs
# def create_transaction
