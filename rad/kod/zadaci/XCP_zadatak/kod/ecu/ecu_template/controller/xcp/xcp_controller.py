from ecu_template.controller.controller import Controller
from ecu_template.handler.xcp.xcp_handler import XCPHandler
from ecu_template.listener.xcp.xcp_listener import XCPListener
from ecu_template.notifier.xcp.xcp_notifier import XCPNotifier


class XCPController(Controller):
    class XCPBusListener(XCPListener):
        def __init__(self, handler: XCPHandler):
            super().__init__()
            self.handler = handler

        def on_message_received(self, msg):
            self.handler.handle_msg(msg)

    def __init__(self, handler: XCPHandler, notifier: XCPNotifier):
        self.notifier = notifier
        self.listener = self.XCPBusListener(handler)
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
