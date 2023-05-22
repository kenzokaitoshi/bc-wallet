"""class that defines electronic or digital transactions"""
import datetime

from neon_wallet.transaction.transaction import Transaction


class ETransaction(Transaction):
    """class DigitalTransaction"""

    # Define the constructor that takes the amount as a parameter,
    # the type and currency of the operation
    def __init__(
        self,
        amount: float,
        _type: str,
        currency: str,
    ) -> None:
        # Check that the amount is a positive or zero number
        if amount >= 0:
            # Assign the amount to the amount attribute
            self.amount = amount
        else:
            # Throw ValueError if amount is negative
            raise ValueError("Amount must be positive or zero")

        # Check that the type is a string among
        # "deposit", "withdraw" or "convert"
        if (
            _type
            and isinstance(_type, str)
            and _type in ["deposit", "withdraw", "convert"]
        ):
            # Assign type to type attribute
            self.type = _type
        else:
            # Throw ValueError if type is invalid
            raise ValueError("Type must be 'deposit', 'withdraw' or 'convert'")

        # Check that the currency is a string
        # not empty if type is "convert"
        if _type == "convert":
            if currency and isinstance(currency, str):
                # Assign the currency to the currency attribute
                self.currency = currency
            else:
                # Throw a ValueError exception if the currency
                # is empty or not a string
                raise ValueError("Currency must be a non-empty string")
        else:
            # Assign None to the currency attribute
            self.currency = ""

        # Assign the current date and time to the date attribute
        self.date = datetime.datetime.now()
