"""test wallet class"""

from neon_wallet.wallet.coin_wallet import CoinWallet
from neon_wallet.wallet.core import wallet
from neon_wallet.wallet.e_wallet import EWallet
from neon_wallet.wallet.ether_wallet import EtherWallet


def test_convert_balance_to() -> None:
    """test convert balance from currency to new currency"""
    wallet = CoinWallet()
    wallet.balance = 50
    devise_origine, devise_cible = "BTC", "EUR"
    solde_cad = wallet.convert_balance_to(devise_origine, devise_cible)
    assert True is isinstance(solde_cad, float)
    # this value is not constant, the currency conversion changes constantly
    # assert round(solde_cad, 1) == 1254143.7


def test_convert_wallet_balance() -> None:
    """test convert balance from currency to new currency"""
    wallet = CoinWallet()
    wallet.balance = 50
    devise_origine, devise_cible = "BTC", "EUR"
    solde_cad = wallet.convert(devise_origine, devise_cible)
    assert True is isinstance(solde_cad, float)
    # this value is not constant, the currency conversion changes constantly
    # assert round(solde_cad, 1) == 1250381.2


def test_instanciation_of_wallet() -> None:
    """test instanciation of wallet"""
    _w = wallet("EUR")

    # Check type of inherited class
    assert False is isinstance(_w, EtherWallet)  # False
    assert False is isinstance(_w, CoinWallet)  # False
    assert True is isinstance(_w, EWallet)  # True
