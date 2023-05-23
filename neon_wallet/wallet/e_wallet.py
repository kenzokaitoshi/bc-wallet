"""Currency wallet class"""

import time
from typing import Any, List

import ecdsa
import requests

from neon_wallet.transaction.fiduciary.e_transaction import (
    ETransaction as Transaction,
)
from neon_wallet.wallet.wallet import Wallet


class EWallet(Wallet[Transaction]):
    """Currency wallet class"""

    url: str = ""  # API url to send transaction to the recipient

    # Define the constructor that takes the amount as a parameter
    # initial in a particular currency
    def __init__(self, symbol: str, amount: float = 0) -> None:
        super(EWallet, self).__init__(symbol)
        # Generate a pair of public and private keys using the SECP256k1 curve
        self.private_key = self.generate_private_key()
        self.public_key = self.private_key.get_verifying_key()
        # Check that the amount is a positive or zero number
        self.symbol = symbol
        self.transactions: List[Transaction] = []
        if amount >= 0:
            # Assign the amount to the balance attribute
            self.balance = amount
        else:
            # Throw ValueError if amount is negative
            raise ValueError("Amount must be positive or zero")

    # Define a method that returns the balance of the wallet
    # according to the currency
    def get_account_balance(self) -> float:
        """get account balance"""
        # Return the balance attribute
        return self.balance

    # Define a function to read the private key from a file
    def get_private_from_wallet(self) -> Any:
        """get private from wallet"""
        return self.private_key.to_string().hex()

    # Define a function to get the public key from
    # of the private key
    def get_public_from_wallet(self) -> Any:
        """get public from wallet"""
        return "04" + self.public_key.to_string().hex()

    # Define a function to generate a random private key
    def generate_private_key(self) -> Any:
        """generate private key"""
        return ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

    # Define a function to delete the wallet
    def delete_wallet(self) -> None:
        """delete wallet"""

    # Define a method that adds an amount of a currency to the wallet balance
    def deposit(self, amount: float) -> None:
        """method that add amount of one currency in the balance"""
        # Check that the amount is a positive or zero number
        if amount >= 0:
            # Add amount to balance attribute
            self.balance += amount
            # Create a "deposit" type transaction with
            # the amount and the currency
            transaction = Transaction(amount, "deposit", self.symbol)
            # Add the transaction to the list of wallet transactions
            self.transactions.append(transaction)
        else:
            # Throw ValueError if amount is negative
            raise ValueError("Amount must be positive or zero")

    # Define a method that withdraws an amount from the currency
    # current wallet balance
    def withdraw(self, amount: float) -> None:
        """method that withdraw money to the wallet balance"""
        # Check that the amount is a positive or zero number
        if amount >= 0:
            # Check that the balance is sufficient to make the withdrawal
            if self.balance >= amount:
                # Subtract amount from balance attribute
                self.balance -= amount
            else:
                # Throw a RuntimeError exception if the balance
                # is insufficient
                raise RuntimeError("Insufficient balance")
        else:
            # Throw ValueError if amount is negative
            raise ValueError("Amount must be positive or zero")

    def convert(self, base: str, currency: str) -> float:
        """convert wallet currency to another currency"""
        return self.convert(base, currency)

    # Define a method that sends an amount in euros to another
    # wallet address
    def send_transaction(
        self,
        address: str,
        amount: float,
    ) -> Transaction:
        """send transaction to recipient"""
        # Check that the amount is a positive or zero number
        if amount >= 0:
            # Check that the recipient's address is a string
            # of characters not empty and valid
            if (
                address
                and isinstance(address, str)
                and len(address) == 66
                and address.startswith("04")
            ):
                # Check that the balance of the wallet is sufficient to
                # perform the transfer
                if self.balance >= amount:
                    # Withdraw amount from wallet balance
                    self.withdraw(amount)
                    # Define a transaction as a dictionary
                    transaction = {
                        # The address of the wallet sending the funds
                        "sender": self.get_public_from_wallet(),
                        # The address of the wallet receiving the funds
                        "recipient": address,
                        # The transaction amount
                        "amount": amount,
                        # The transaction time in seconds
                        "timestamp": int(time.time()),
                    }
                    # Convert transaction to string
                    message = str(transaction)
                    # Sign the transaction with the private key of the wallet
                    signature = self.private_key.sign(message.encode())
                    # Add signature to transaction
                    transaction["signature"] = signature.hex()
                    # Define the URL of the API which allows to send
                    # network transactions
                    # Make a POST request to the URL with the
                    # transaction as data
                    response = requests.post(
                        self.url,
                        data=transaction,
                        timeout=60,
                    )
                    # Check that the response contains the "success" key
                    if "success" in response.json():
                        # Check that the value of the "success" key is True
                        if response.json()["success"]:
                            # Return True if the send was successful
                            return Transaction(amount, "withdraw", self.symbol)
                        else:
                            # Throw RuntimeError if sending
                            # failed
                            raise RuntimeError("Sending failed")
                    else:
                        # Throw a RuntimeError exception if the response
                        # does not contain the expected key
                        raise RuntimeError("Invalid response")
                else:
                    # Throw a RuntimeError exception if the balance
                    # is insufficient
                    raise RuntimeError("Insufficient balance")
            else:
                # Throw a ValueError exception if the address of the recipient
                # is empty, invalid or not a string
                msg_error = "Recipient must be a non-empty and valid string"
                raise ValueError(msg_error)
        else:
            # Throw ValueError if amount is negative
            raise ValueError("Amount must be positive or zero")

    # Define a method that displays wallet transactions
    def show_transactions(self) -> None:
        """show transaction"""
        # Check that the list of transactions is not empty
        if self.transactions:
            # Display a message indicating the number of transactions
            print(f"This wallet have {len(self.transactions)} transactions:")
            # Browse transaction list
            for transaction in self.transactions:
                # Display information of each transaction:
                # date, type, amount and currency
                _t = transaction.type
                _m = transaction.amount
                _p = f"the {transaction.date:%d/%m/%Y à %H:%M:%S},{_t} of {_m}"
                print(_p)
                # If the transaction type is "convert", also display
                # the balance converted into the target currency
                if transaction.type == "convert":
                    _op = transaction.amount
                    print(f"Balance convert: {_op:.2f} {transaction.currency}")
        else:
            # Display a message indicating that the wallet does not have
            # of transactions
            print("This wallet has no transactions.")
