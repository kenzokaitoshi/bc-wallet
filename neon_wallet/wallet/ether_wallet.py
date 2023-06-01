"""Ethereum wallet class"""
from typing import Any, Dict
from eth_account import Account
from web3 import Web3


class EtherWallet:
    """Ethereum wallet class"""

    url: str = "http://127.0.0.1:7545"
    address: Any
    balance: float
    gas_limit: int = 2000000
    gas_price: str = "50"

    # Define the constructor that generates a private/public key pair
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.private_key = self.get_private_from_wallet()
        self.web3 = Web3(Web3.HTTPProvider(self.url))

    def get_account_balance(self) -> Any:
        """get account balance"""
        balance = self.web3.eth.get_balance(self.address)
        return self.web3.from_wei(balance, "ether")

    # Define a method that converts the private key to hexadecimal format
    def get_private_from_wallet(self) -> Any:
        """get private key from wallet"""
        account = Account()
        return account.create().key.hex()

    # Define a method that generates an ethereum address
    # at start from the public key
    def generate_address(self) -> Any:
        """generate address"""
        public_address = self.web3.eth.account.from_key(self.private_key)
        # Get public address from a signer wallet
        self.address = public_address.address
        return self.address

    # Define a method that signs a transaction using the private key
    # of the wallet
    def sign_transaction(self, _tx: Dict[str, Any], priv_key: Any) -> Any:
        """sign transaction"""
        return self.web3.eth.account.sign_transaction(_tx, priv_key)

    # Define a method that creates an ethereum transaction
    # from a Wallet object
    def create_transaction(
        self,
        nonce: int,
        gas_price: Any,
        receiver_address: Any,
        value: float,
        gas_limit: int = 2000000,
    ) -> Dict[str, Any]:
        """create transaction"""
        return {
            "nonce": nonce,
            "to": receiver_address,
            "value": self.web3.to_wei(value, "ether"),
            "gas": gas_limit,
            "gasPrice": self.web3.to_wei(gas_price, "gwei"),
        }

    def send_transaction(self, recipient_address: str, amount: int) -> Any:
        """send trx"""
        nonce = self.web3.eth.get_transaction_count(self.address)

        _tx = self.create_transaction(
            nonce,
            self.gas_price,
            recipient_address,
            amount,
            self.gas_limit,
        )

        signed_tx = self.sign_transaction(_tx, self.private_key)

        return self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
