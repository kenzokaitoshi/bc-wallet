"""abstract wallet class"""

from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar, Generic

T = TypeVar("T")


class Wallet(Generic[T], object, metaclass=ABCMeta):
    """Wallet abstract class"""

    def __init__(self, symbol: str) -> None:
        # symbol define the type currency like Euro, BTC ...etc
        self.symbol = symbol
        self.symbol_native = "€"

    # Define a function to read the private key from a file
    @abstractmethod
    def get_private_from_wallet(self) -> str:
        """get private from wallet"""
        raise NotImplementedError

    # Define a function to get the public key from
    # of the private key
    @abstractmethod
    def get_public_from_wallet(self) -> Any:
        """get public from wallet"""
        raise NotImplementedError

    # Define a function to generate a random private key
    @abstractmethod
    def generate_private_key(self) -> Any:
        """generate private key"""
        raise NotImplementedError

    # Define a function to initialize the wallet
    @abstractmethod
    def init_wallet(self) -> None:
        """initialize wallet"""
        raise NotImplementedError

    # Define a function to delete the wallet
    @abstractmethod
    def delete_wallet(self) -> None:
        """delete wallet"""
        raise NotImplementedError

    # Define a function to get account balance
    @abstractmethod
    def get_account_balance(self) -> float:
        """get account balance"""
        raise NotImplementedError

    # Define a function to send a transaction
    @abstractmethod
    def send_transaction(self, address: str, amount: float) -> T:
        """send transaction"""
        raise NotImplementedError
