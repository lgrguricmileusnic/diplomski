from scapy.contrib.automotive.xcp.xcp import XCPOnCAN

from ecu_template.handler.xcp.xcp_handler import XCPHandler
from impl.ecu_model import ECUModelImpl


class XCPHandlerImpl(XCPHandler):
    def __init__(self, ecu: ECUModelImpl):
        super().__init__(ecu)

    def handle_msg(self, msg: XCPOnCAN):
        pass
