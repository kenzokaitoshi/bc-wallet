"""helpers test module transaction pool"""
import ecdsa
from neon_wallet.transaction.transaction import Transaction
from neon_wallet.transaction.tx_in import TxIn
from neon_wallet.transaction.tx_out import TxOut


private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
public_key = private_key.get_verifying_key()

# Convert the public key to a hex string for the address
address = public_key.to_string().hex()


def seeder() -> Transaction:
    """seeder"""
    # Create a transaction input that references this unspent output
    tx_in = TxIn("1234", 0, "")

    # Create a new transaction that contains this transaction entry
    # and an arbitrary transaction output
    _tx = Transaction(
        [tx_in],
        [
            TxOut(
                "04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a",
                50,
            )
        ],
    )

    # Sign the transaction entry with the private key and id of
    # the transaction
    tx_in.signature = private_key.sign(bytes.fromhex(_tx.id)).hex()

    return _tx
