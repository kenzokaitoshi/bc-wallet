"""test eallet class"""
from neon_wallet.wallet.e_wallet import EWallet as Wallet


def test_withdraw_deposit() -> None:
    """test withdraw"""
    wallet1 = Wallet("EUR", 100)
    wallet2 = Wallet("EUR", 50)
    wallet1.withdraw(20)
    wallet2.deposit(20, 'EUR')
    assert wallet1.get_account_balance() == 80
    assert wallet2.get_account_balance() == 70


def test_get_account_balance() -> None:
    """get account balance"""
    wallet1 = Wallet("EUR", 100)
    assert wallet1.get_account_balance() == 100
