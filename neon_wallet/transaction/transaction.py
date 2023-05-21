"""abstract class of Transaction"""

from abc import ABCMeta


class Transaction(object, metaclass=ABCMeta):
    """Wallet abstract class"""

    def __init__(self) -> None:
        raise NotImplementedError
