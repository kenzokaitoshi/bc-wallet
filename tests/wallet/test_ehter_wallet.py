"""unit test for ethereum wallet"""

from neon_wallet.wallet.ether_wallet import EtherWallet


wallet = EtherWallet("ETH")


def test_get_private_from_wallet() -> None:
    """test get private from wallet"""
    private_key_hex = wallet.get_private_from_wallet()
    assert len(private_key_hex) == 64


def test_get_public_from_wallet() -> None:
    """test get public from wallet"""
    public_key_hex = wallet.get_public_from_wallet()
    assert len(public_key_hex) == 64


def test_generate_address() -> None:
    """test generate address"""
    address = wallet.generate_address()
    assert len(address) == 42
    assert True is isinstance(address, str)
    assert True is str(address).startswith("0x")


def test_sign_message() -> None:
    """test sign message"""
    message = "Bonjour, monde !"
    signature = wallet.sign_message(message)
    assert True is len(signature) != 0


def test_verify_signature() -> None:
    """test verify signature"""
    message = "Bonjour, monde !"
    signature = wallet.sign_message(message)
    result = wallet.verify_signature(message, signature)
    assert True is result
