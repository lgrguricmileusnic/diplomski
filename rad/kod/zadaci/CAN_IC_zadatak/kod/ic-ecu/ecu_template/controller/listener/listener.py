from abc import ABCMeta, abstractmethod


class PacketListener(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def on_message_received(self, packet):
        pass
