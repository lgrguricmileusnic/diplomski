from scapy.layers.can import CAN

from ecu_template.handler.can.can_handler import CanHandler
from impl.ecu_model import ECUModelImpl


class SpeedData:
    def __init__(self, data: bytes):
        self.speed = int(data[2:3])


class CanHandlerImpl(CanHandler):
    def __init__(self, ecu: ECUModelImpl):
        super().__init__(ecu)

    def handle_msg(self, msg: CAN):
        if msg.data:
            pass
