from scapy.contrib.automotive.uds import UDS

from ecu_template.controller.controller import Controller
from ecu_template.controller.listener.uds.uds_listener import UDSListener
from ecu_template.handler.uds.uds_handler import UDSHandler
from ecu_template.notifier.uds.uds_notifier import UDSNotifier


class UDSController(Controller):
    class UDSIsoTpListener(UDSListener):
        def __init__(self, handler: UDSHandler):
            super().__init__()
            self.handler = handler

        def on_message_received(self, packet: UDS):
            self.handler.handle_msg(packet)

    def __init__(self, handler: UDSHandler, notifier: UDSNotifier):
        self.notifier = notifier
        self.handler = handler
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        self.notifier.add_listener(self.UDSIsoTpListener(self.handler))
        self.notifier.start()

    def stop(self):
        if not self.running:
            return
        self.notifier.stop()
