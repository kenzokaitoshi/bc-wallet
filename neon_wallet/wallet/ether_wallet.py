"""Ethereum wallet class"""
from typing import Any
import hashlib
import ecdsa
import eth_utils


class EtherWallet:
    """Ethereum wallet class"""

    # Define the constructor that generates a private/public key pair
    def __init__(self, symbol: str) -> None:
        # Generate private key from secp256k1 curve
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        # Generate public key from private key
        self.public_key = self.private_key.get_verifying_key()
        # Generate an ethereum address from the public key
        self.address = self.generate_address()
        self.symbol = symbol

    # Define a method that converts the private key to hexadecimal format
    def get_private_from_wallet(self) -> Any:
        """get private key from wallet"""
        # Get private key bytes
        private_key_bytes = self.private_key.to_string()
        # Encode the key in hexadecimal to obtain the hex format
        private_key_hex = private_key_bytes.hex()
        # Return the hex key as a string
        return private_key_hex

    # Define a method that converts the public key
    # in hexadecimal format
    def get_public_from_wallet(self) -> Any:
        """get public key from wallet"""
        # Get public key bytes
        public_key_bytes = self.public_key.to_string()
        # Add the prefix 0x04 to indicate a public key
        # uncompressed
        public_key_extended = b"\x04" + public_key_bytes
        # Encode extended key in hexadecimal to get hex format
        public_key_hex = public_key_extended.hex()
        # Return the hex key as a string
        return public_key_hex

    # Define a method that generates an ethereum address at
    # start from the public key
    def generate_address(self) -> Any:
        """generate address"""
        # Get public key bytes
        public_key_bytes = self.public_key.to_string()
        # Add the prefix 0x04 to indicate a public key
        # uncompressed
        public_key_extended = b"\x04" + public_key_bytes
        # Calculate the Keccak-256 hash of the extended key
        _hash = hashlib.new("keccak_256", public_key_extended)
        public_key_hash = _hash.digest()
        # Take last 20 bytes of hash as raw address
        address_raw = public_key_hash[-20:]
        # Add the 0x prefix to indicate a network address
        # main (mainnet)
        address_prefixed = b"\x00" + address_raw
        # Calculate address checksum using EIP-55 function
        address_checksummed = eth_utils.to_checksum_address(address_prefixed)
        # Return the address as a string
        return address_checksummed

    # Define a method that signs a message with the private key
    def sign_message(self, message: str) -> Any:
        """sign message"""
        try:
            # Convert message to bytes
            message_bytes = message.encode()
            # Calculate the Keccak-256 hash of the message
            message_hash = hashlib.new("keccak_256", message_bytes).digest()
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
