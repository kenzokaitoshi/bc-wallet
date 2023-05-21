"""test transaction pool module"""
from neon_wallet.transaction.coins.coin_transaction import (
    CoinTransaction as Transaction,
)
from neon_wallet.transaction_pool.transaction_pool import TransactionPool
from tests.transaction.helpers_tests import seeder
from tests.transaction_pool.helpers import tx_pool_seeder


def test_get_transaction_pool() -> None:
    """test get transaction pool"""
    txp = TransactionPool()
    tx_pools = txp.get_transaction_pool()
    assert True is isinstance(tx_pools, list)
    assert len(tx_pools) == 0
    txp.transaction_pool.append(tx_pool_seeder())
    tx_pools = txp.get_transaction_pool()
    assert True is all([isinstance(tx, Transaction) for tx in tx_pools])


def test_add_to_transaction_pool() -> None:
    """test add to transaction pool method"""
    txp = TransactionPool()
    _tx, unspent_tx_outs = seeder()[0], seeder()[1]
    txp.add_to_transaction_pool(_tx, unspent_tx_outs)
    tx_pools = txp.get_transaction_pool()
    assert len(tx_pools) != 0
    assert True is all([isinstance(tx, Transaction) for tx in tx_pools])


def test_is_invalid_tx_for_pool() -> None:
    """test is valid tx for pool: check txIn already found in the txPool"""
    txp = TransactionPool()
    _tx = seeder()[0]
    txp.transaction_pool.append(_tx)
    at_transaction_pool = txp.get_transaction_pool()
    assert False is txp.is_valid_tx_for_pool(_tx, at_transaction_pool)


def test_get_tx_pool_ins() -> None:
    """test get_tx_pool_ins function"""
    txp = TransactionPool()
    _tx = seeder()[0]
    txp.transaction_pool.append(_tx)
    tx_pools = txp.get_transaction_pool()
    assert True is all([isinstance(tx, Transaction) for tx in tx_pools])


def test_has_tx_in() -> None:
    """test has_tx_in function"""
    txp = TransactionPool()
    unspent_tx_outs, _txin = seeder()[1], seeder()[2]
    assert True is txp.has_tx_in(_txin, unspent_tx_outs)
