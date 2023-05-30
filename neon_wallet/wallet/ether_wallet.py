"""Ethereum wallet class"""
from typing import Any
import secrets
import sha3
import hashlib
from eth_keys import keys
import ecdsa


class EtherWallet:
    """Ethereum wallet class"""

    # Define the constructor that generates a private/public key pair
    def __init__(self, symbol: str) -> None:
        # Generate private key from secp256k1 curve
        self.private_key = self.get_private_from_wallet()
        # Generate public key from private key
        self.public_key = self.get_public_from_wallet()
        # Generate an ethereum address from the public key
        self.address = self.generate_address()
        self.symbol = symbol

    # Define a method that converts the private key to hexadecimal format
    def get_private_from_wallet(self) -> Any:
        """get private key from wallet"""
        return "{:64x}".format(secrets.randbits(256))

    # Define a method that converts the public key
    # in hexadecimal format
    def get_public_from_wallet(self) -> Any:
        """get public key from wallet"""
        private_key_bytes = bytes.fromhex(self.private_key)
        return keys.PrivateKey(private_key_bytes).public_key

    # Define a method that generates an ethereum address at
    # start from the public key
    def generate_address(self) -> Any:
        """generate address"""
        public_key = self.get_public_from_wallet()
        public_key_bytes = bytes.fromhex(str(public_key)[2:])

        return keys.PublicKey(public_key_bytes).to_address()

    # Define a method that signs a message with the private key
    def sign_message(self, message: str) -> Any:
        """sign message"""
        try:
            # Convert message to bytes
            message_bytes = message.encode()
            # Calculate the Keccak-256 hash of the message
            keccak = sha3.keccak_256()
            keccak.update(message_bytes)
            message_hash = keccak.digest()
            # Sign the hash with the private key using
            # the ECDSA algorithm
            signature = self.private_key.sign_digest(
                message_hash, sigencode=ecdsa.util.sigencode_der
            )
            # Return signature as bytes
            return signature
        except ecdsa.BadSignatureError:
            return None

    # Define a method that verifies the signature of a message
    # with the public key
    def verify_signature(self, message: str, signature: str) -> Any:
        """verify signature"""
        try:
            # Convert message to bytes
            message_bytes = message.encode()
            # Calculate the Keccak-256 hash of the message
            message_hash = hashlib.new("keccak_256", message_bytes).digest()
            # Verify signature with public key using
            # the ECDSA algorithm
            result = self.public_key.verify_digest(
                signature, message_hash, sigdecode=ecdsa.util.sigdecode_der
            )
            # Return the result in boolean form
            return result
        except ecdsa.BadSignatureError:
            return False
