from abc import abstractmethod

from scapy.contrib.automotive.xcp.xcp import XCPOnCAN
from scapy.contrib.cansocket_native import NativeCANSocket

from ecu_template.model.ecu_model import ECUModel
from ..can.can_handler import CanHandler


class XCPHandler(CanHandler):
    def __init__(self, ecu: ECUModel):
        super().__init__(ecu)
        self.socket = None
        self.ecu = ecu

    @abstractmethod
    def handle_msg(self, msg: XCPOnCAN):
        raise NotImplementedError

    def set_socket(self, socket: NativeCANSocket):
        if not socket.basecls == XCPOnCAN:
            raise TypeError
        super().set_socket(socket)
