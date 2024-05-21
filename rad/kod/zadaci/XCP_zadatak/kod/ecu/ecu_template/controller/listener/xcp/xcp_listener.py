from abc import abstractmethod

from scapy.contrib.automotive.xcp.xcp import XCPOnCAN

from ecu_template.controller.listener.listener import PacketListener


class XCPListener(PacketListener):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def on_message_received(self, packet: XCPOnCAN):
        pass
