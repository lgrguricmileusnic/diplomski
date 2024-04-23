import threading

from scapy.contrib.automotive.uds import UDS
from scapy.contrib.isotp.isotp_native_socket import ISOTPNativeSocket

from ecu_template.listener.uds.uds_listener import UDSListener
from ecu_template.notifier.notifier import Notifier

THREAD_NAME = "UDSnotifier"


class UDSNotifier(Notifier):
    def __init__(self, socket: ISOTPNativeSocket):
        if socket is None:
            raise TypeError
        if socket.basecls != UDS:
            raise TypeError
        self.rx_thread = None
        self._running = False
        self.socket = socket
        self.listeners = []

    def _rx_thread(self):
        while self._running:
            try:
                if packet := self.socket.recv():
                    for listener in self.listeners:
                        listener.on_message_received(packet)
            except Exception as e:
                print(e)

    def start(self):
        self._running = True
        self.rx_thread = threading.Thread(target=self._rx_thread, name=THREAD_NAME)
        self.rx_thread.daemon = True
        self.rx_thread.start()

    def stop(self, timeout: float = 5.0):
        self._running = False
        if self.rx_thread is not None:
            self.rx_thread.join(timeout)

    def add_listener(self, listener: UDSListener):
        self.listeners.append(listener)

    def remove_listener(self, listener: UDSListener):
        self.listeners.remove(listener)
