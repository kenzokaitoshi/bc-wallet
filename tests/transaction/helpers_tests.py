"""helpers module transaction"""
# Create dummy data to test the function

# Create an ECDSA private key and public key for the owner
# of an unspent release
from typing import Tuple
import ecdsa
from neon_wallet.transaction.coins.coin_transaction import (
    CoinTransaction as Transaction,
)
from neon_wallet.transaction.coins.tx_in import TxIn
from neon_wallet.transaction.coins.tx_out import TxOut

from neon_wallet.transaction.coins.unspent_tx_out import UnspentTxOut
from tests.helpers_data import (
    tx_out_1,
    tx_ins_sig_1,
    tx_out_adx_1,
    tx_out_adx_2,
    tx_ins_sig_2,
    tx_out_adx_3,
)

private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
public_key = private_key.get_verifying_key()

# Convert the public key to a hex string for the address
address = public_key.to_string().hex()


def unspent_tx_outs() -> list[UnspentTxOut]:
    """get seed of unspent_tx_outs"""
    # Create an unspent exit belonging to this address
    # with an arbitrary amount
    unspent_tx_out = UnspentTxOut("1234", 0, address, 50)

    # Create a list containing this unspent output
    return [unspent_tx_out]


def unspent_tx_outs_of_address(addr: str) -> list[UnspentTxOut]:
    """get seed of unspent_tx_outs"""
    # Create an unspent exit belonging to this address
    # with an arbitrary amount
    unspent_tx_out = UnspentTxOut("1234", 0, addr, 50)

    # Create a list containing this unspent output
    return [unspent_tx_out]


def seeder() -> Tuple[Transaction, list[UnspentTxOut], TxIn]:
    """seeder"""
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
    _tx = Transaction(
        [tx_in],
        [
            TxOut(
                tx_out_1,
                50,
            )
        ],
    )

    # Sign the transaction entry with the private key and id of
    # the transaction
    tx_in.signature = private_key.sign(bytes.fromhex(_tx.id)).hex()

    return _tx, a_unspent_tx_outs, tx_in


# Create some sample transactions and UTXOs for testing
tx1 = Transaction(
    tx_ins=[
        TxIn(
            tx_out_id="tx0",
            tx_out_index=0,
            signature=tx_ins_sig_1,
        )
    ],
    tx_outs=[
        TxOut(
            address=tx_out_adx_1,
            amount=10,
        ),
        TxOut(
            address=tx_out_adx_2,
            amount=20,
        ),
    ],
)
tx2 = Transaction(
    tx_ins=[
        TxIn(
            tx_out_id="tx1",
            tx_out_index=0,
            signature=tx_ins_sig_2,
        )
    ],
    tx_outs=[
        TxOut(
            address=tx_out_adx_3,
            amount=10,
        ),
        TxOut(
            address=tx_out_adx_2,
            amount=20,
        ),
    ],
)


utxo1 = UnspentTxOut(
    tx_out_id="tx0",
    tx_out_index=0,
    address=tx_out_adx_1,
    amount=30.0,
)
utxo2 = UnspentTxOut(
    tx_out_id="tx1",
    tx_out_index=0,
    address=tx_out_adx_2,
    amount=10.0,
)
utxo3 = UnspentTxOut(
    tx_out_id="tx1",
    tx_out_index=1,
    address=tx_out_adx_3,
    amount=20.0,
)
