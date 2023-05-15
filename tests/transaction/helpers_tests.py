"""helpers tests"""
from neon_wallet.transaction.transaction import Transaction
from neon_wallet.transaction.tx_in import TxIn
from neon_wallet.transaction.tx_out import TxOut
from neon_wallet.transaction.unspent_tx_out import UnspentTxOut


# Create some sample transactions and UTXOs for testing
tx1 = Transaction(
    tx_ins=[TxIn(tx_out_id="tx0", tx_out_index=0, signature="sig1")],
    tx_outs=[
        TxOut(address="addr1", amount=10),
        TxOut(address="addr2", amount=20),
    ],
)
tx2 = Transaction(
    tx_ins=[TxIn(tx_out_id="tx1", tx_out_index=0, signature="sig2")],
    tx_outs=[
        TxOut(address="addr3", amount=5),
        TxOut(address="addr4", amount=5),
    ],
)
tx3 = Transaction(
    tx_ins=[TxIn(tx_out_id="tx1", tx_out_index=1, signature="sig3")],
    tx_outs=[
        TxOut(address="addr5", amount=15),
        TxOut(address="addr6", amount=5),
    ],
)

utxo1 = UnspentTxOut(
    tx_out_id="tx0",
    tx_out_index=0,
    address="04b0bd634234abbbcc1ba1e986e884185c61cf43da82f5963a8c70171b1b200c006a8421997ac617d91d406e5fa52bbf4d16e2a069e6b9b668a3935dabaecbc401",
    amount=30.0,
)
utxo2 = UnspentTxOut(
    tx_out_id="tx1",
    tx_out_index=0,
    address="04b0bd634234abbbcc1ba1e986e884185c61cf43da82f5963a8c70171b1b200c006a8421997ac617d91d406e5fa52bbf4d16e2a069e6b9b668a3935dabaecbc402",
    amount=10.0,
)
utxo3 = UnspentTxOut(
    tx_out_id="tx1",
    tx_out_index=1,
    address="04b0bd634234abbbcc1ba1e986e884185c61cf43da82f5963a8c70171b1b200c006a8421997ac617d91d406e5fa52bbf4d16e2a069e6b9b668a3935dabaecbc403",
    amount=20.0,
)
utxo4 = UnspentTxOut(
    tx_out_id="tx2",
    tx_out_index=0,
    address="04b0bd634234abbbcc1ba1e986e884185c61cf43da82f5963a8c70171b1b200c006a8421997ac617d91d406e5fa52bbf4d16e2a069e6b9b668a3935dabaecbc404",
    amount=5.0,
)
utxo5 = UnspentTxOut(
    tx_out_id="tx2",
    tx_out_index=1,
    address="04b0bd634234abbbcc1ba1e986e884185c61cf43da82f5963a8c70171b1b200c006a8421997ac617d91d406e5fa52bbf4d16e2a069e6b9b668a3935dabaecbc405",
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
