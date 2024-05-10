from scapy.layers.can import CAN

from ecu_template.handler.can.can_handler import CanHandler
from impl.ecu_model import ECUModelImpl


class CanHandlerImpl(CanHandler):
    def __init__(self, ecu: ECUModelImpl):
        super().__init__(ecu)

    def handle_msg(self, msg: CAN):
        print(msg.identifier)
        msg.identifier += 1
        self.socket.send(msg)
