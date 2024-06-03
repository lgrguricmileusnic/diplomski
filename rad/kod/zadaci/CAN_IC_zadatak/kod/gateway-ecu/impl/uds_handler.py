from time import *

from scapy.contrib.automotive.uds import *
from scapy.contrib.cansocket_native import NativeCANSocket
from scapy.layers.can import *

from ecu_template.handler.uds.uds_handler import UDSHandler
from ecu_template.model.ecu_model import ECUModel


class UDSHandlerImpl(UDSHandler):
    def __init__(self, ecu: ECUModel):
        super().__init__(
            ecu,
        )

    @staticmethod
    def _speed_demo(sock: NativeCANSocket):
        data = bytearray(3)
        data[0] = 0xAB
        data[1] = 0x00
        data[2] = 0x00
        while True:
            p = CAN(identifier=0x456, data=data)
            sock.send(p)
            if data[2] + 25 > 175:
                break
            data[2] += 25
            time.sleep(1)

    @staticmethod
    def _blinkers_and_dash_demo(sock: NativeCANSocket):
        data = bytearray(2)
        data[0] = 0xBB
        data[1] = 0x01
        for i in range(8):
            p = CAN(identifier=0x456, data=data)
            sock.send(p)
            if data[1] == 32:
                return
            data[1] <<= 1
            time.sleep(1)

    def handle_msg(self, msg: UDS):
        match msg.payload:
            case UDS_ER():
                self.isotp.send(UDS() / UDS_ERPR(resetType=msg.resetType))
            case UDS_DSC():
                self.isotp.send(
                    UDS() / UDS_DSCPR(diagnosticSessionType=msg.diagnosticSessionType)
                )
            case UDS_RC():
                can_socket = NativeCANSocket(channel=self.isotp.iface)
                self.isotp.send(
                    UDS()
                    / UDS_RCPR(
                        routineControlType=msg.payload.routineControlType,
                        routineIdentifier=msg.payload.routineIdentifier,
                    )
                )
                self._speed_demo(can_socket)
                self._blinkers_and_dash_demo(can_socket)
