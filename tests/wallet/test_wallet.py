"""test wallet class"""

from neon_wallet.wallet.coin_wallet import CoinWallet
from neon_wallet.wallet.e_wallet import EWallet
from neon_wallet.wallet.ether_wallet import EtherWallet
from neon_wallet.wallet.wallet import Wallet


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
    _w = Wallet("ETH")

    # Conditionner l'héritage multiple en fonction du symbole
    if _w.symbol == "ETH":
        _w.__class__ = EtherWallet
    elif _w.symbol in ["BTC", "LIC", "BC"]:
        _w.__class__ = CoinWallet
    elif _w.symbol in ["EUR", "CFA", "US", "YEN"]:
        _w.__class__ = EWallet

    # Vérifier le type de la classe héritée
    assert True is isinstance(_w, EtherWallet)  # True
    assert False is isinstance(_w, CoinWallet)  # False
    assert False is isinstance(_w, EWallet)  # False