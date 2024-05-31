from abc import abstractmethod

from scapy.layers.can import CAN

from ecu_template.listener.listener import PacketListener


class CanListener(PacketListener):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def on_message_received(self, packet: CAN):
        pass
