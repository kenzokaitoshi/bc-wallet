"""p2p class file"""
import socket
from typing import Any, Dict, List

from neon_wallet.blockchain.block import Block
from neon_wallet.p2p.Message import Message


class P2P:
    """p2p class"""

    def init_p2p_server(self, p2p_port: int) -> None:
        """init p2p server"""

    def get_sockets(self) -> socket:
        """get sockets"""

    def init_connection(self, _ws: socket) -> None:
        """initConnection"""

    def json_to_object(self, data: str) -> Dict[str, Any]:
        """JSONToObject"""

    def init_message_handler(self, _ws: socket) -> None:
        """init message handler"""

    def write(self, _ws: socket, message: Message) -> None:
        """write"""

    def broadcast(self, message: Message) -> None:
        """broadcast"""

    def query_chain_length_msg(self) -> Message:
        """query chain length msg"""

    def query_all_msg(self) -> Message:
        """query all msg"""

    def response_chain_msg(self) -> Message:
        """response chain msg"""

    def response_latest_msg(self) -> Message:
        """response latest msg"""

    def query_transaction_pool_msg(self) -> Message:
        """query transaction pool msg"""

    def response_transaction_pool_msg(self) -> Message:
        """response transaction pool msg"""

    def init_error_handler(self, _ws: socket) -> None:
        """init error handler"""

    def close_connection(self, my_ws: socket) -> None:
        """close connection"""

    def handle_blockchain_response(self, received_blocks: List[Block]) -> None:
        """handle blockchain response"""

    def broadcast_latest(self) -> None:
        """broadcast latest"""

    def connect_to_peers(self, new_peer: str) -> None:
        """connect to peers"""

    def broad_cast_transaction_pool(self) -> None:
        """broad cast transaction pool"""
