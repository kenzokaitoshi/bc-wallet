"""p2p class file"""
import json
import socket
from typing import Any, Dict, List

from neon_wallet.blockchain.block import Block
from neon_wallet.p2p.Message import Message


sockets = []


class MessageType:
    QUERY_LATEST = 0
    QUERY_ALL = 1
    RESPONSE_BLOCKCHAIN = 2
    QUERY_TRANSACTION_POOL = 3
    RESPONSE_TRANSACTION_POOL = 4


class P2P:
    """p2p class"""

    def init_p2p_server(self, p2p_port: int) -> None:
        """init p2p server"""
        server = socket.create_connection(p2p_port)
        server.on('connection', self.init_connection())
        print('listening websocket p2p port on: ' + p2p_port)

    def get_sockets(self) -> socket:
        """get sockets"""
        return sockets

    def init_connection(self, _ws: socket) -> None:
        """initConnection"""
        _ws.on('message', (lambda data: self.handle_message(_ws, data)))

    def json_to_object(self, data: str) -> Dict[str, Any]:
        """JSONToObject"""
        try:
            return json.loads(data)
        except Exception as e:
            print(e)
            return None

    def initMessageHandler(self, _ws: socket) -> None:
        """init message handler"""
        _ws.on('message', (lambda data: self.handleMessage(_ws, data)))

    def handle_message(self, ws, data):
        try:
            message = self.json_to_object(data)
            if message is None:
                print('could not parse received JSON message: ' + data)
                return
            print('Received message: %s' % json.dumps(message))
            if message['type'] == MessageType.QUERY_LATEST:
                self.write(ws, self.response_latest_msg())
            elif message['type'] == MessageType.QUERY_ALL:
                self.write(ws, self.response_chain_msg())
            elif message['type'] == MessageType.RESPONSE_BLOCKCHAIN:
                receivedBlocks = self.json_to_object(message['data'])
                if receivedBlocks is None:
                    print('invalid blocks received: %s' %
                          json.dumps(message['data']))
                else:
                    self.handle_blockchain_response(receivedBlocks)
            elif message['type'] == MessageType.QUERY_TRANSACTION_POOL:
                self.write(ws, self.response_transaction_pool_msg())
            elif message['type'] == MessageType.RESPONSE_TRANSACTION_POOL:
                receivedTransactions = self.json_to_object(message['data'])
                if receivedTransactions is None:
                    print('invalid transaction received: %s' %
                          json.dumps(message['data']))
                else:
                    for transaction in receivedTransactions:
                        try:
                            self.handle_received_transaction(transaction)
                            # if no error is thrown, transaction was indeed added to the pool
                            # let's broadcast transaction pool
                            self.broad_cast_transaction_pool()
                        except Exception as e:
                            print(e.message)
        except Exception as e:
            print(e)

    def write(self, _ws: socket, message: Message) -> None:
        """write"""
        _ws.send(json.dumps(message))

    def broadcast(self, message: Message) -> None:
        """broadcast"""
        for socket in sockets:
            self.write(socket, message)

    def query_chain_length_msg(self) -> Message:
        """query chain length msg"""
        return Message(MessageType.QUERY_LATEST, None)

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
