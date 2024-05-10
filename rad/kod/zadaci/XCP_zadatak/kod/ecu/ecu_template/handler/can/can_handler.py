from abc import abstractmethod

from scapy.contrib.cansocket_native import NativeCANSocket
from scapy.layers.can import CAN

from ecu_template.model.ecu_model import ECUModel
from ..handler import Handler


class CanHandler(Handler):
    def __init__(self, ecu: ECUModel):
        super().__init__()
        self.socket = None
        self.ecu = ecu

    @abstractmethod
    def handle_msg(self, msg: CAN):
        raise NotImplementedError

    def set_socket(self, socket: NativeCANSocket):
        self.socket = socket
