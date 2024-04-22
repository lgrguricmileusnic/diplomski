from abc import ABCMeta, abstractmethod

from scapy.layers.can import CAN


class CanListener(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def on_message_received(self, packet: CAN):
        pass
