from scapy.contrib.automotive.uds import *

from ecu_template.handler.uds.uds_handler import UDSHandler
from impl.ecu_model import ECUModelImpl


def _get_size_from_UDS_RMBA(msg: UDS_RMBA):
    match msg.memorySizeLen:
        case 1:
            return msg.memorySize1
        case 2:
            return msg.memorySize2
        case 3:
            return msg.memorySize3
        case 4:
            return msg.memorySize4


class UDSHandlerImpl(UDSHandler):
    def __init__(self, ecu: ECUModelImpl):
        if not isinstance(ecu, ECUModelImpl):
            raise TypeError

        super().__init__(
            ecu,
        )
        self.callbacks: dict = {UDS_RMBA: self._handle_UDS_RMBA,
                                UDS_ER: self._handle_UDS_ER,
                                UDS_DSC: self._handle_UDS_DSC}
        # IDs discoverable by caringcaribou
        self.discoverable_service_ids = [0x10, 0x11, 0x23]

    def handle_msg(self, msg: UDS):
        msg_type = type(msg.payload)
        if msg_type is NoPayload and msg.service in self.discoverable_service_ids:
            # for a service to be discoverable by carincaribou, it needs to respond with a positive response or
            # a negative response with response code != 0x11 (0x11 = serviceNotSupported)
            # https://github.com/CaringCaribou/caringcaribou/blob/master/caringcaribou/modules/uds.py#L364
            self._send_UDS_NR(msg, 0x01)
        if msg_type in self.callbacks:
            self.callbacks[msg_type](msg)
        else:
            self._send_UDS_NR(msg, 0x11)

    def _handle_UDS_RMBA(self, msg: UDS):
        # Address must be 32bit
        if msg.memoryAddressLen != 4:
            self._send_UDS_NR(msg, 0x13)
            return

        size = _get_size_from_UDS_RMBA(msg)
        address = msg.memoryAddress4
        try:
            self.isotp.send(UDS() / UDS_RMBAPR(dataRecord=self.ecu.get_data_from_memory(address, size)))
        except IndexError:
            self._send_UDS_NR(msg, 0x31)

    def _handle_UDS_ER(self, msg):
        # simulate reset
        self.isotp.send(UDS() / UDS_ERPR(resetType=msg.resetType))

    def _handle_UDS_DSC(self, msg):
        # caringcaribou discovery reply
        self.isotp.send(
            UDS() / UDS_DSCPR(diagnosticSessionType=msg.diagnosticSessionType)
        )

    def _send_UDS_NR(self, msg, code):
        self.isotp.send(UDS() / UDS_NR(requestServiceId=msg.service, negativeResponseCode=code))
