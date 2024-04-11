import can
from typing import Callable, Awaitable

class RawCanHandler():
    
    class CanHandlerListener(can.Listener):
        def __init__(self):
            self.callbacks = {}

        def on_message_received(self, msg: can.Message):
            if msg.arbitration_id in self.callbacks.keys():
                for callback in self.callbacks[msg.arbitration_id]:
                    callback(msg)

        def add_callback_for_id(self, rx_callback: Callable[[can.Message], Awaitable[None] | None], arb_id: int):
            if arb_id not in self.callbacks.keys():
                self.callbacks[arb_id] = []
            self.callbacks[arb_id].append(rx_callback)
        
        def remove_callback_for_id(self, rx_callback: Callable[[can.Message], Awaitable[None] | None], arb_id: int):
            if arb_id in self.callbacks.keys:
                self.callbacks[arb_id].remove(rx_callback)

    def __init__(self, interface: str):
        self.bus = can.Bus(interface, "socketcan", ignore_config=True)
        self.notifier = can.Notifier(self.bus, [])
        self.listener = self.CanHandlerListener()

    def add_callback_for_id(self, rx_callback: Callable[[can.Message], Awaitable[None] | None], arb_id: int):
        self.listener.add_callback_for_id(rx_callback, arb_id)
    
    def remove_callback_for_id(self, rx_callback: Callable[[can.Message], Awaitable[None] | None], arb_id: int):
        self.listener.remove_callback_for_id(rx_callback, arb_id)

    def start(self):
        self.notifier.add_listener(self.listener)
    
    def stop(self):
        self.notifier.stop()
        self.bus.shutdown()