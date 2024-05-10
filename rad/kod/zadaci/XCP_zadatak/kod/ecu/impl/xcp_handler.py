from scapy.contrib.automotive.xcp.cto_commands_master import *
from scapy.contrib.automotive.xcp.cto_commands_slave import *
from scapy.contrib.automotive.xcp.xcp import XCPOnCAN

from ecu_template.handler.xcp.xcp_handler import XCPHandler
from impl.ecu_model import ECUModelImpl


class XCPHandlerImpl(XCPHandler):
    def __init__(self, ecu: ECUModelImpl):
        super().__init__(ecu)
        self.req_id = 0x700
        self.res_id = 0x701

    def handle_msg(self, msg: XCPOnCAN):
        print(msg)
        if isinstance(msg.payload.pid, ShortUpload):
            self._send(ShortUploadPositiveResponse(element="flag{AAAAA}"))

    def _send(self, msg_payload):
        self.socket.send(XCPOnCAN(identifier=self.res_id) / msg_payload)
