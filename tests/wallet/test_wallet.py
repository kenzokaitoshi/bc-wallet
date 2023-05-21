# Import
from neon_wallet.wallet.bitcoin_wallet import CoinWallet


def test_convert_balance_to() -> None:
    """test convert balance from currency to new currency"""
    wallet = CoinWallet()
    wallet.balance = 50
    devise_origine, devise_cible = "BTC", "EUR"
    solde_cad = wallet.convert_balance_to(devise_origine, devise_cible)
    assert True is isinstance(solde_cad, float)
    assert round(solde_cad, 1) == 1254143.7


def test_convert_wallet_balance() -> None:
    """test convert balance from currency to new currency"""
    wallet = CoinWallet()
    wallet.balance = 50
    devise_origine, devise_cible = "BTC", "EUR"
    solde_cad = wallet.convert(devise_origine, devise_cible)
    assert True is isinstance(solde_cad, float)
    assert round(solde_cad, 1) == 1250381.2
