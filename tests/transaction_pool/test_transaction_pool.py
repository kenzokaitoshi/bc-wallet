"""test transaction pool module"""
from neon_wallet.transaction.transaction import Transaction
from neon_wallet.transaction_pool.transaction_pool import TransactionPool
from tests.transaction_pool.helpers import seeder


def test_get_transaction_pool() -> None:
    """test get transaction pool"""
    txp = TransactionPool()
    tx_pools = txp.get_transaction_pool()
    assert True is isinstance(tx_pools, list)
    assert len(tx_pools) == 0
    txp.transaction_pool.append(seeder())
    tx_pools = txp.get_transaction_pool()
    assert True is all([isinstance(tx, Transaction) for tx in tx_pools])
