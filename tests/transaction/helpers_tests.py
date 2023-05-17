# Create dummy data to test the function

# Create an ECDSA private key and public key for the owner of an unspent release
import ecdsa
from neon_wallet.transaction.transaction import Transaction
from neon_wallet.transaction.tx_in import TxIn
from neon_wallet.transaction.tx_out import TxOut

from neon_wallet.transaction.unspent_tx_out import UnspentTxOut


private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
public_key = private_key.get_verifying_key()

# Convert the public key to a hex string for the address
address = public_key.to_string().hex()


# Create some sample transactions and UTXOs for testing
tx1 = Transaction(
    tx_ins=[
        TxIn(
            tx_out_id="tx0",
            tx_out_index=0,
            signature="dfb6a9666227cf04f830534dcaba295309e24db466d2880181d931440f9b929a",
        )
    ],
    tx_outs=[
        TxOut(
            address="04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a",
            amount=10,
        ),
        TxOut(
            address="04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534b",
            amount=20,
        ),
    ],
)
tx2 = Transaction(
    tx_ins=[
        TxIn(
            tx_out_id="tx1",
            tx_out_index=0,
            signature="80a18b8de39288b15bc1caacfddca6fc92846b343d137918f6aa2df7f2089785cb41b5ef00a46f8e70cb2a3a61da2b099590c91722088a43d5bbd3c24a104622",
        )
    ],
    tx_outs=[
        TxOut(
            address="04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534d",
            amount=10,
        ),
        TxOut(
            address="04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534c",
            amount=20,
        ),
    ],
)
tx3 = Transaction(
    tx_ins=[
        TxIn(
            tx_out_id="tx1",
            tx_out_index=1,
            signature="80a18b8de39288b15bc1caacfddca6fc92846b343d137918f6aa2df7f2089785",
        )
    ],
    tx_outs=[
        TxOut(
            address="04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534d",
            amount=10,
        ),
        TxOut(
            address="04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534c",
            amount=20,
        ),
    ],
)

utxo1 = UnspentTxOut(
    tx_out_id="tx0",
    tx_out_index=0,
    address="04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a",
    amount=30.0,
)
utxo2 = UnspentTxOut(
    tx_out_id="tx1",
    tx_out_index=0,
    address="04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a",
    amount=10.0,
)
utxo3 = UnspentTxOut(
    tx_out_id="tx1",
    tx_out_index=1,
    address="04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a",
    amount=20.0,
)
utxo4 = UnspentTxOut(
    tx_out_id="tx2",
    tx_out_index=0,
    address="04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a",
    amount=5.0,
)
utxo5 = UnspentTxOut(
    tx_out_id="tx2",
    tx_out_index=1,
    address="04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a",
    amount=5.0,
)
utxo6 = UnspentTxOut(
    tx_out_id="tx3",
    tx_out_index=0,
    address="04b0bd634234abbbcc1ba1e986e884185c61cf43da82f5963a8c70171b1b200c006a8421997ac617d91d406e5fa52bbf4d16e2a069e6b9b668a3935dabaecbc406",
    amount=15.0,
)
utxo7 = UnspentTxOut(
    tx_out_id="tx3",
    tx_out_index=1,
    address="04b0bd634234abbbcc1ba1e986e884185c61cf43da82f5963a8c70171b1b200c006a8421997ac617d91d406e5fa52bbf4d16e2a069e6b9b668a3935dabaecbc407",
    amount=5.0,
)
