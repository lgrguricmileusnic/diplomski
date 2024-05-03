from scapy.contrib.automotive.uds import *

from ecu_template.handler.uds.uds_handler import UDSHandler
from impl.ecu_model import ECUModelImpl

import hashlib
import os


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
                                UDS_RDBI: self._handle_UDS_RDBI,
                                UDS_SA: self._handle_UDS_SA}
        # IDs discoverable by caringcaribou
        self.discoverable_service_ids = [0x10, 0x11, 0x22, 0x23, 0x27]
        self.dbi: dict = {self.DBI_VIN: 0x9,
                          self.DBI_CTF_HINT: 0x21}
        self.sa_requests: dict = {}
        self.sa_unlocked = False

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

    def _handle_UDS_SA(self, msg: UDS):
        if msg.securityAccessType % 2 == 1:
            # requestSeed
            seed = os.urandom(16)
            hf = hashlib.sha512()
            hf.update(seed)
            key = hf.digest()
            self.sa_requests[msg.securityAccessType] = (seed, key)
            self.isotp.send(UDS() / UDS_SAPR(securityAccessType=msg.securityAccessType, securitySeed=seed))
        else:
            # sendKey
            request_seed_access_type = (msg.securityAccessType - 1)
            if request_seed_access_type not in self.sa_requests.keys():
                print("UDS SA request sequence")
                self._send_UDS_NR(msg, 0x24)  # 0x24 requestSequenceError
                return

            client_key = msg.securityKey
            if client_key != self.sa_requests[request_seed_access_type][1]:
                print("UDS SA invalid key!")
                self._send_UDS_NR(msg, 0x35)  # 0x35 invalidKeyError
            self.sa_unlocked = True
            self.sa_requests.pop(request_seed_access_type)
            print("Unlocked!")
            self.isotp.send(UDS() / UDS_SAPR(securityAccessType=msg.securityAccessType))

    def _handle_UDS_RDBI(self, msg: UDS):
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
        if not self.sa_unlocked:
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
