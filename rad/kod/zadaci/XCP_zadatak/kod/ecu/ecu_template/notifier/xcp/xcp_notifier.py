import threading

from scapy.contrib.cansocket_native import NativeCANSocket

from ecu_template.listener.xcp.xcp_listener import XCPListener
from ..notifier import Notifier

THREAD_NAME = "XCPNotifier"


class XCPNotifier(Notifier):
    def __init__(self, socket: NativeCANSocket):
        if socket is None:
            raise TypeError
        self.rx_thread = None
        self._running = False
        self.socket = socket
        self.listeners = []

    def _rx_thread(self):
        while self._running:
            if packet := self.socket.recv():
                for listener in self.listeners:
                    listener.on_message_received(packet)

    def start(self):
        self._running = True
        self.rx_thread = threading.Thread(target=self._rx_thread, name=THREAD_NAME)
        self.rx_thread.daemon = True
        self.rx_thread.start()

    def stop(self, timeout: float = 1.0):
        self._running = False
        if self.rx_thread is not None:
            self.rx_thread.join(timeout)

    def add_listener(self, listener: XCPListener):
        self.listeners.append(listener)

    def remove_listener(self, listener: XCPListener):
        self.listeners.remove(listener)
