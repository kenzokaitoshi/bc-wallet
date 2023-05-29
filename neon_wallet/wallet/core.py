"""core"""


import json
from typing import Any
from neon_wallet.wallet.coin_wallet import CoinWallet
from neon_wallet.wallet.e_wallet import EWallet

from neon_wallet.wallet.ether_wallet import EtherWallet


def wallet(symbol: str) -> Any:
    """Wallet"""

    # Condition multiple inheritance based on symbol
    if symbol == "ETH":
        return EtherWallet(symbol)
    elif symbol in ["BTC", "BCH", "LTC", "DASH", "ZEC", "BSV"]:
        return CoinWallet(symbol)
    elif get_currency(symbol):
        return EWallet(symbol)


def get_currency(currency: str) -> bool:
    """get currency"""
    path = "data/Common-Currency.json"
    is_true = False

    file = open(path, encoding="utf-8")
    for key in json.load(file).keys():
        is_true = False if key == currency else True

    return is_true
