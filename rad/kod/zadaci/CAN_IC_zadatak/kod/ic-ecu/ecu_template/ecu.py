from scapy.contrib.automotive.uds import UDS
from scapy.contrib.automotive.xcp.xcp import XCPOnCAN
from scapy.contrib.cansocket_native import NativeCANSocket
from scapy.contrib.isotp.isotp_native_socket import ISOTPNativeSocket

from ecu_template.controller.can.can_controller import CanController
from ecu_template.controller.uds.uds_controller import UDSController
from ecu_template.notifier.uds.uds_notifier import UDSNotifier
from .controller.xcp.xcp_controller import XCPController
from .handler.can.can_handler import CanHandler
from .handler.uds.uds_handler import UDSHandler
from .handler.xcp.xcp_handler import XCPHandler
from .notifier.can.can_notifier import CanNotifier
from .notifier.xcp.xcp_notifier import XCPNotifier


class ECU:
    def __init__(
        self,
        interface: str,
        canfd: bool,
        can_handler: CanHandler,
        can_filters: list,
        uds_handler: UDSHandler,
        uds_config: dict,
        xcp_handler: XCPHandler,
        xcp_config: list,
    ):

        self.controllers = []
        if can_handler is not None:
            can_socket = NativeCANSocket(channel=interface, can_filters=can_filters)
            can_handler.set_socket(can_socket)
            self.controllers.append(CanController(can_handler, CanNotifier(can_socket)))

        if uds_handler is not None and uds_config is not None:
            isotp_socket = ISOTPNativeSocket(
                iface=interface,
                basecls=UDS,
                rx_id=uds_config["rx_id"],
                tx_id=uds_config["tx_id"],
                fd=canfd,
            )
            uds_handler.set_socket(isotp_socket)
            self.controllers.append(
                UDSController(uds_handler, UDSNotifier(socket=isotp_socket))
            )
        if xcp_handler is not None and xcp_config is not None:
            xcp_socket = NativeCANSocket(
                channel=interface, can_filters=xcp_config, basecls=XCPOnCAN
            )
            xcp_handler.set_socket(xcp_socket)
            self.controllers.append(
                XCPController(xcp_handler, XCPNotifier(socket=xcp_socket))
            )

    def start(self):
        for controller in self.controllers:
            controller.start()

    def stop(self):
        for controller in self.controllers:
            controller.stop()
