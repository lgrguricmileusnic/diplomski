from scapy.contrib.automotive.uds import *

from ecu_template.handler.uds.uds_handler import UDSHandler
from ecu_template.model.ecu_model import ECUModel


class UDSHandlerImpl(UDSHandler):
    def __init__(self, ecu: ECUModel):
        super().__init__(
            ecu,
        )

    def handle_msg(self, msg: UDS):
        match msg.payload:
            case UDS_ER():
                self.isotp.send(UDS() / UDS_ERPR(resetType=msg.resetType))
            case UDS_DSC():
                self.isotp.send(
                    UDS() / UDS_DSCPR(diagnosticSessionType=msg.diagnosticSessionType)
                )
