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
                                UDS_DSC: self._handle_UDS_DSC,
                                UDS_RDBI: self._handle_UDS_RDBI}
        # IDs discoverable by caringcaribou
        self.discoverable_service_ids = [0x10, 0x11, 0x22, 0x23]
        self.dbi: dict = {self.DBI_VIN: 0x9,
                          self.DBI_CTF_HINT: 0x21}

    class DBI_VIN(Packet):
        # https://scapy.readthedocs.io/en/latest/layers/automotive.html#customization-of-uds-rdbi-uds-wdbi
        name = "DataByIdentifier_VIN_Packet"
        fields_desc = [
            StrField('vin', b"", fmt="B")
        ]

    class DBI_CTF_HINT(Packet):
        # https://scapy.readthedocs.io/en/latest/layers/automotive.html#customization-of-uds-rdbi-uds-wdbi
        name = "DataByIdentifier_CTF_Hint_Packet"
        fields_desc = [
            StrField('hint', b"", fmt="B")
        ]

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

    def _handle_UDS_SA(self):
        pass

    def _handle_UDS_RDBI(self, msg: UDS):
        rdbi = msg.payload
        if not isinstance(rdbi, UDS_RDBI):
            return
        res = UDS()
        if len(set(self.dbi.values()).intersection(set(msg.identifiers))) <= 0:
            self._send_UDS_NR(msg, 0x31)
        for identifier in msg.identifiers:
            if identifier == self.dbi[self.DBI_VIN]:
                self.isotp.send(res /
                                UDS_RDBIPR(dataIdentifier=self.dbi[self.DBI_VIN]) /
                                self.DBI_VIN(vin=self.ecu.vin)
                                )
            elif identifier == self.dbi[self.DBI_CTF_HINT]:
                self.isotp.send(res /
                                UDS_RDBIPR(dataIdentifier=self.dbi[self.DBI_CTF_HINT]) /
                                self.DBI_CTF_HINT(hint="SHA-512")
                                )

    def _handle_UDS_RMBA(self, msg: UDS):
        if not self.ecu.sa_unlocked:
            # SecurityAccessDenied
            self._send_UDS_NR(msg, 0x33)

        # Address must be 32bit
        if msg.memoryAddressLen != 4 or msg.memorySizeLen != 1:
            self._send_UDS_NR(msg, 0x13)
            return

        size = _get_size_from_UDS_RMBA(msg)
        address = msg.memoryAddress4
        try:
            data = self.ecu.get_data_from_memory(address, size)
            if len(data) == 0:
                self._send_UDS_NR(msg, 0x31)
            else:
                self.isotp.send(UDS() / UDS_RMBAPR(dataRecord=data))
        except Exception:
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

    def _init_DBI_packets(self):
        for pkt_cls, identifier in self.dbi.items():
            bind_layers(UDS_RDBIPR, pkt_cls, dataIdentifier=identifier)
            bind_layers(UDS_WDBI, pkt_cls, dataIdentifier=identifier)
            UDS_RDBI.dataIdentifiers[identifier] = pkt_cls.name[:-7]  # strip _Packet
