"""wallet module"""
# Import ecdsa library to use secp256k1 curve
import json
import os
from typing import Any, List

# Import copy module to clone objects
import copy
import ecdsa


# Import pydash library to use functions
# similar to lodash
import pydash

from neon_wallet.transaction.coins.coin_transaction import (
    CoinTransaction as Transaction,
)
from neon_wallet.transaction.coins.transactions import (
    get_public_key,
    get_transaction_id,
    sign_tx_in,
)
from neon_wallet.transaction.coins.tx_in import TxIn

from neon_wallet.transaction.coins.tx_out import TxOut
from neon_wallet.transaction.coins.unspent_tx_out import UnspentTxOut
from neon_wallet.transaction_pool.transaction_pool import TransactionPool
from neon_wallet.wallet.wallet import Wallet

PRIVATE_KEY = "node/wallet/private_key"


class CoinWallet(Wallet[Transaction]):
    """wallet class"""

    # Create an ECDSA object from the secp256k1 curve
    EC = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

    # Set private key location
    privateKeyLocation = os.environ.get("PRIVATE_KEY") or "{PRIVATE_KEY}"
    unspent_tx_outs: List[UnspentTxOut] = []

    def __init__(self, symbol: str = "BTC") -> None:
        super(CoinWallet, self).__init__(symbol)
        self.symbol = symbol

    # Define a function to read the private key from a file
    def get_private_from_wallet(self) -> str:
        """get private from wallet"""
        # Open file in read and binary mode
        with open(self.privateKeyLocation, "rb") as file:
            # Read file contents and convert to string of characters
            buffer = file.read()
            return buffer.decode()

    # Define a function to replace the list of UnspentTxOuts
    # by a new list
    def set_unspent_tx_outs(
        self,
        new_unspent_tx_out: List[UnspentTxOut],
    ) -> None:
        """set unspent tx outs"""
        # Display the new list of UnspentTxOuts
        print(f"replacing unspentTxouts with: {new_unspent_tx_out}")
        # Assign the new list to the unspentTxOuts global variable
        self.unspent_tx_outs = new_unspent_tx_out

    # Define a function to get the public key from
    # of the private key
    def get_public_from_wallet(self) -> Any:
        """get public from wallet"""
        # Call the getPrivateFromWallet function to read the private key
        private_key = self.get_private_from_wallet()
        # Create an ECDSA object from the private key in hexadecimal
        key = ecdsa.SigningKey.from_string(
            bytes.fromhex(private_key), curve=ecdsa.SECP256k1
        )
        # Obtain the corresponding public key and encode it
        # in compressed hexadecimal
        return key.get_verifying_key().to_string("compressed").hex()

    # Define a function to generate a random private key
    def generate_private_key(self) -> Any:
        """generate private key"""
        # Create an ECDSA object from the secp256k1 curve
        key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        # Get the private key as a string
        # in hexadecimal
        return key.to_string().hex()

    # Define a function to initialize the wallet
    def init_wallet(self) -> None:
        """init wallet"""
        pr_key_loc = self.privateKeyLocation
        # Do not overwrite existing private keys
        if os.path.exists(pr_key_loc):
            return
        # Generate a new private key
        new_private_key = self.generate_private_key()
        # Write the private key to the file
        with open(pr_key_loc, "w", encoding="utf8") as file:
            file.write(new_private_key)
        # Display a message indicating the location of the file
        print(f"nouveau portefeuille avec clé privée créé à : {pr_key_loc}")

    # Define a function to delete the wallet
    def delete_wallet(self) -> None:
        """delete wallet"""
        # If the file exists, delete it
        if os.path.exists(self.privateKeyLocation):
            os.remove(self.privateKeyLocation)

    # Define a function to get the balance of an address from
    # of unspent outputs
    def get_balance(
        self,
        address: str,
        unspent_tx_outs: List[UnspentTxOut],
    ) -> Any:
        """get balance"""
        # Find unspent outputs that belong to the address
        unspent_tx_outs = pydash.filter_(
            unspent_tx_outs, lambda uTxO: uTxO.address == address
        )
        # Extract amounts from unspent outputs
        amounts = pydash.map_(unspent_tx_outs, lambda uTxO: uTxO.amount)
        # Sum the amounts
        return pydash.sum_(amounts)

    # Define a function to get account balance
    def get_account_balance(self) -> float:
        """get account balance"""
        # Retrieve the public key of the wallet
        public_key = self.get_public_from_wallet()
        # Retrieve list of UnspentTxOuts
        unspent_tx_outs = self.get_unspent_tx_outs()
        # Return account balance based on public key
        # and UnspentTxOuts
        return float(self.get_balance(public_key, unspent_tx_outs))

    # Define a function to get the list of UnspentTxOuts
    def get_unspent_tx_outs(self) -> List[UnspentTxOut]:
        """get unspent transaction outs"""
        # Return a deep copy of the list of UnspentTxOuts
        return copy.deepcopy(self.unspent_tx_outs)

    def get_my_unspent_transaction_outputs(self) -> Any:
        """get my unspent transaction outputs"""
        return self.find_unspent_tx_outs(
            self.get_public_from_wallet(),
            self.get_unspent_tx_outs(),
        )

    # Define a function to send a transaction
    def send_transaction(self, address: str, amount: float) -> Transaction:
        """send transaction"""
        tx_pool = TransactionPool()
        # Create transaction with address, amount, private key
        # of the wallet, the list of UnspentTxOuts and the pool of
        # transactions
        _tx = self.create_transaction(
            address,
            amount,
            self.get_private_from_wallet(),
            self.get_unspent_tx_outs(),
            tx_pool.get_transaction_pool(),
        )
        # Add transaction to transaction pool
        tx_pool.add_to_transaction_pool(_tx, self.get_unspent_tx_outs())
        # Return created transaction
        return _tx

    # Define a function to find unspent outputs that
    # belong to an address
    def find_unspent_tx_outs(
        self, owner_address: str, unspent_tx_outs: List[UnspentTxOut]
    ) -> Any:
        """find unspent tx outs"""
        # Filter unspent outputs by address
        return pydash.filter_(
            unspent_tx_outs,
            lambda uTxO: uTxO.address == owner_address,
        )

    # Define a function to find the outputs of
    # transactions for a given amount
    def find_tx_outs_for_amount(
        self, amount: float, my_unspent_tx_outs: List[UnspentTxOut]
    ) -> Any:
        """find tx outs for amount"""
        # Initialize the current amount and the list of outputs of
        # transactions included
        current_amount: float = 0
        included_unspent_tx_outs = []
        # Browse unspent transaction outputs
        for my_unspent_tx_out in my_unspent_tx_outs:
            # Add transaction output to list
            included_unspent_tx_outs.append(my_unspent_tx_out)
            # Increase the current amount with the amount
            # of transaction output
            current_amount += my_unspent_tx_out.amount
            # If the current amount is greater than or equal to
            # the requested amount
            if current_amount >= amount:
                # Calculer le montant restant
                left_over_amount = current_amount - amount
                # Return a dictionary with transaction outputs
                # included and the remaining amount
                return {
                    "includedUnspentTxOuts": included_unspent_tx_outs,
                    "leftOverAmount": left_over_amount,
                }

        # If the requested amount is not reached, raise an exception
        # with an error message
        _e = "Cannot create transaction from the available unspent tx outputs."
        e_msg = (
            _e
            + " Required amount:"
            + str(amount)
            + ". Available unspentTxOuts:"
            + str(my_unspent_tx_outs)
        )
        raise ValueError(e_msg)

    # Define a function to create transaction outputs
    def create_tx_outs(
        self,
        receiver_address: str,
        my_address: str,
        amount: float,
        left_over_amount: float,
    ) -> List[TxOut]:
        """create Tx Outs"""
        # Create transaction output for receiver
        # with the requested amount
        tx_out1 = TxOut(receiver_address, amount)
        # If the remaining amount is zero
        if left_over_amount == 0:
            # Return a list with transaction output
            # for recipient
            return [tx_out1]
        # else
        else:
            # Create transaction output for self
            # with remaining amount
            left_over_tx = TxOut(my_address, left_over_amount)
            # Return a list with both transaction outputs
            return [tx_out1, left_over_tx]

    # Define a function to filter out UnspentTxOuts that
    # are used in the transaction pool
    def filter_tx_pool_txs(
        self,
        unspent_tx_outs: List[UnspentTxOut],
        transaction_pool: List[Transaction],
    ) -> List[UnspentTxOut]:
        """filter TxPool Txs"""
        # Create an empty list to store transaction pool txIns
        tx_ins = []
        # Browse pool transactions
        for _tx in transaction_pool:
            # Add the txIns of each transaction to the list
            tx_ins.extend(_tx.tx_ins)

        # Create an empty list to store UnspentTxOuts to remove
        removable = []
        # Browse existing UnspentTxOuts
        for unspent_tx_out in unspent_tx_outs:
            # Check if there is a txIn that matches the UnspentTxOut
            tx_in = next(
                (
                    aTxIn
                    for aTxIn in tx_ins
                    if aTxIn.tx_out_index == unspent_tx_out.tx_out_index
                    and aTxIn.tx_out_id == unspent_tx_out.tx_out_id
                ),
                None,
            )
            # If there is a corresponding txIn, add the UnspentTxOut
            # to the list to remove
            if tx_in is not None:
                removable.append(unspent_tx_out)

        # Create an empty list to store filtered UnspentTxOuts
        filtered = []
        # Browse existing UnspentTxOuts
        for unspent_tx_out in unspent_tx_outs:
            # If the UnspentTxOut is not in the list to remove,
            # add it to the filtered list
            if unspent_tx_out not in removable:
                filtered.append(unspent_tx_out)

        return filtered

    # Define a function to create a transaction
    def create_transaction(
        self,
        receiver_address: str,
        amount: float,
        private_key: str,
        unspent_tx_outs: List[UnspentTxOut],
        tx_pool: List[Transaction],
    ) -> Transaction:
        """create transaction"""
        print(f"txPool: {json.dumps(tx_pool)}")
        # Retrieve the address of the creator of the transaction
        # from his private key
        my_address = get_public_key(private_key)
        # Filter UnspentTxOuts that belong to the
        # transaction creator
        my_unspent_tx_outs_a = [
            uTxO for uTxO in unspent_tx_outs if uTxO.address == my_address
        ]
        # Filter UnspentTxOuts which are not used in the pool
        # of transactions
        my_unspent_tx_outs = self.filter_tx_pool_txs(
            my_unspent_tx_outs_a,
            tx_pool,
        )

        # Find sufficient UnspentTxOuts to cover the amount of
        # the transaction and the rest
        i_uto, l_oam = self.find_tx_outs_for_amount(amount, my_unspent_tx_outs)
        included_unspent_tx_outs, left_over_amount = i_uto, l_oam

        # Create a function to convert an UnspentTxOut to a
        # Unsigned TxIn
        def to_unsigned_tx_in(unspent_tx_out: UnspentTxOut) -> TxIn:
            """to unsigned tx in"""
            tx_in = TxIn("", 0, "")
            tx_in.tx_out_id = unspent_tx_out.tx_out_id
            tx_in.tx_out_index = unspent_tx_out.tx_out_index
            return tx_in

        # Create a list of unsigned TxIns from
        # of UnspentTxOuts found
        i_uns_tx_outs = included_unspent_tx_outs
        unsigned_tx_ins = [to_unsigned_tx_in(uTxO) for uTxO in i_uns_tx_outs]

        # Create a new transaction
        _tx = Transaction([], [])
        _tx.tx_ins = unsigned_tx_ins
        _tx.tx_outs = self.create_tx_outs(
            receiver_address,
            my_address,
            amount,
            left_over_amount,
        )
        _tx.id = get_transaction_id(_tx)

        # Sign TxIns with the private key of the creator of the transaction
        _tx.tx_ins = [
            sign_tx_in(_tx, index, private_key, unspent_tx_outs)
            for index in range(len(_tx.tx_ins))
        ]

        return _tx
