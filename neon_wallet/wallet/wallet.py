"""abstract wallet class"""

from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar, Generic

# Import the requests module to make HTTP requests
import requests

T = TypeVar("T")


class Wallet(Generic[T], object, metaclass=ABCMeta):
    """Wallet abstract class"""

    def __init__(self, symbol: str) -> None:
        # symbol define the type currency like Euro, BTC ...etc
        self.symbol = symbol
        self.balance = 0.0

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

    # Define a method that converts the wallet balance
    # in another currency
    def convert(self, base: str, currency: str) -> float:
        """convert currency to"""
        # Check that the currency is a non-empty string
        if currency and isinstance(currency, str):
            # Convert currency to uppercase
            currency = currency.upper()
            # Define the URL of the API which provides the exchange rates
            uri = f"https://api.exchangerate.host/latest?base={base}&symbols="
            url = uri + currency
            # Make a GET request to the URL and get the response as
            # dictionary form
            response = requests.get(url, timeout=60).json()
            # Check that the response contains the "success" and "rates" keys
            if "success" in response and "rates" in response:
                # Check that the value of the "success" key is True
                # and the "rates" key contains the requested currency
                if response["success"] and currency in response["rates"]:
                    # Get the exchange rate between the euro and the currency
                    # requested
                    rate = response["rates"][currency]
                    # Calculate and return the balance converted to
                    # multiplying by the exchange rate
                    return self.balance * float(rate)
                else:
                    # Throw a RuntimeError exception if the request
                    # failed or if the requested currency is not available
                    msg_error = "Conversion failed or currency not available"
                    raise RuntimeError(msg_error)
            else:
                # Throw a RuntimeError exception if the response does not
                # does not contain expected keys
                raise RuntimeError("Invalid response")
        else:
            # Throw ValueError if currency is empty
            # or is not a string
            raise ValueError("Currency must be a non-empty string")

    # Define a method that takes the balance as a parameter Portfolio
    # Home Currency and Target Currency
    def convert_balance_to(self, origin: str, cible: str) -> float:
        """convert balance from origin currency to target currency"""
        # Build the api url with parameters
        solde = self.balance
        uri = "https://api.exchangerate.host/convert"
        url = f"{uri}?from={origin}&to={cible}&amount={solde}"
        # Make a GET request to the api and get the response
        response = requests.get(url, timeout=60)
        print("response", response)
        # Check response status
        if response.status_code == 200:
            # Convert response to JSON
            data = response.json()
            print("data: ", data)
            # Extract the converted balance
            balance_convert = data["result"]
            print(balance_convert)
            # Return the converted balance
            return float(str(balance_convert))
        else:
            # Return an error code
            print(f"Erreur: {response.status_code}")
            return response.status_code
