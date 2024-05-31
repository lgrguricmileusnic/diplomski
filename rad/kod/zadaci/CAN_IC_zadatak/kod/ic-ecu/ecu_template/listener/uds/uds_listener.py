from abc import abstractmethod

from scapy.contrib.automotive.uds import UDS

from ecu_template.listener.listener import PacketListener


class UDSListener(PacketListener):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def on_message_received(self, packet: UDS):
        pass
