from abc import ABCMeta, abstractmethod

from scapy.contrib.automotive.uds import UDS


class UDSListener(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def on_message_received(self, packet: UDS):
        pass
