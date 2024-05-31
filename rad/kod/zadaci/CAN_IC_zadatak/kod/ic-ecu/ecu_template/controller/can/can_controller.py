from scapy.layers.can import CAN

from ecu_template.controller.controller import Controller
from ecu_template.controller.listener.can.can_listener import CanListener
from ecu_template.handler.can.can_handler import CanHandler
from ecu_template.notifier.can.can_notifier import CanNotifier


class CanController(Controller):
    class CanBusListener(CanListener):
        def __init__(self, handler: CanHandler):
            super().__init__()
            self.handler = handler

        def on_message_received(self, msg: CAN):
            self.handler.handle_msg(msg)

    def __init__(self, handler: CanHandler, notifier: CanNotifier):
        self.notifier = notifier
        self.listener = self.CanBusListener(handler)
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        self.notifier.add_listener(self.listener)
        self.notifier.start()

    def stop(self):
        if not self.running:
            return
        self.notifier.stop()
