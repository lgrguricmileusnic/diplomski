from abc import abstractmethod

from scapy.contrib.automotive.uds import UDS
from scapy.contrib.isotp.isotp_native_socket import ISOTPNativeSocket

from ecu_template.model.ecu_model import ECUModel
from ..handler import Handler


class UDSHandler(Handler):
    def __init__(self, ecu: ECUModel):
        super().__init__()
        self.ecu = ecu
        self.isotp = None

    @abstractmethod
    def handle_msg(self, msg: UDS):
        raise NotImplementedError

    def set_socket(self, isotp_socket: ISOTPNativeSocket):
        if isotp_socket.basecls != UDS:
            raise TypeError
        self.isotp = isotp_socket
