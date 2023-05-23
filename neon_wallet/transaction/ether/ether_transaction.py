"""ethereum transaction class"""
# Import the eth_account module to create and sign
# of ethereum transactions
from typing import Any
import eth_account

from neon_wallet.wallet.ether_wallet import EtherWallet as Wallet


class Transaction:
    """Define the EtherTransaction class"""

    # Define the constructor that takes the attributes as parameters
    # of an ethereum transaction
    def __init__(
        self,
        nonce: int,
        gas_price: float,
        gas_limit: int,
        to: Any,
        value: float,
        data: Any,
    ) -> None:
        # Assign attributes to object
        # The number of transactions already sent by the sender account
        self.nonce = nonce
        # The price of gas in wei per unit of gas
        self.gas_price = gas_price
        # The maximum amount of gas to be consumed by the transaction
        self.gas_limit = gas_limit
        # The address of the recipient account
        self.to = to
        # The amount in wei to be transferred to the recipient
        self.value = value
        # Optional data associated with the transaction
        self.data = data

    # Define a method that creates an ethereum transaction
    # from a Wallet object
    def create_transaction(self, wallet: Wallet) -> Any:
        """create transaction"""
        # Check that the wallet is an instance of the Wallet class
        if isinstance(wallet, Wallet):
            # Create an Account object from the private key of the wallet
            eth_acc = eth_account.Account()
            account = eth_acc.from_key(
                wallet.get_private_from_wallet(),
            )
            # Create transaction_dict object from attributes
            # Transaction
            transaction_dict = {
                "nonce": self.nonce,
                "gasPrice": self.gas_price,
                "gas": self.gas_limit,
                "to": self.to,
                "value": self.value,
                "data": self.data,
            }
            # Sign the transaction with the Account object and
            # return a SignedTransaction object
            signed_transaction = account.sign_transaction(transaction_dict)
            return signed_transaction
        else:
            # Raise a TypeError exception if the wallet is not
            # an instance of the Wallet class
            raise TypeError("wallet must be an instance of Wallet class")

    # Define a method that verifies the signature of a
    # ethereum transaction with a Wallet object
    def verify_transaction(self, wallet: Wallet) -> Any:
        """verify transaction"""
        # Check that the wallet is an instance of the Wallet class
        if isinstance(wallet, Wallet):
            # Create a SignedTransaction object from the method
            # create_transaction
            signed_transaction = self.create_transaction(wallet)
            # Get the hexadecimal signature of the object
            # SignedTransaction
            signature_hex = signed_transaction.signature.hex()
            # Retrieve the hexadecimal address of the wallet
            address_hex = wallet.address.lower()
            # Check that the signature matches the address
            # using the eth_account module and returning a boolean
            account = eth_account.Account()
            return (
                account.recover_message(
                    self.data.encode(), signature=signature_hex
                )
                == address_hex
            )
        else:
            # Raise a TypeError exception if the wallet is not a
            # instance of the Wallet class
            raise TypeError("wallet must be an instance of Wallet class")
