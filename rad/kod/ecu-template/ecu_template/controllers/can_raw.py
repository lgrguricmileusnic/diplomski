import can
from typing import Callable
from ..models.ecu_model import ECUModel
from .controller import Controller


class CanController(Controller):
    class CanHandlerListener(can.Listener):
        def __init__(self, bus: can.BusABC, model: ECUModel):
            super().__init__(None, None)
            self.bus = bus
            self.model = model
            self.callbacks = {}

        def on_message_received(self, msg: can.Message):
            if msg.arbitration_id in self.callbacks.keys():
                for callback in self.callbacks[msg.arbitration_id]:
                    callback(msg, self.bus, self.model)

        def add_callback_for_id(self, rx_callback: Callable[[can.Message, can.BusABC, ECUModel], None], arb_id: int):
            if arb_id not in self.callbacks.keys():
                self.callbacks[arb_id] = []
            self.callbacks[arb_id].append(rx_callback)

        def remove_callback_for_id(self, rx_callback: Callable[[can.Message, can.BusABC, ECUModel], None], arb_id: int):
            if arb_id in self.callbacks.keys:
                self.callbacks[arb_id].remove(rx_callback)

    def __init__(self, bus: can.BusABC, model: ECUModel):
        self.bus = bus
        self.notifier = can.Notifier(self.bus, [])
        self.ecu = model
        self.listener = self.CanHandlerListener(self.bus, self.ecu)
        self.running = False

    def add_callback_for_id(self, rx_callback: Callable[[can.Message, can.BusABC, ECUModel], None], arb_id: int):
        self.listener.add_callback_for_id(rx_callback, arb_id)

    def remove_callback_for_id(self, rx_callback: Callable[[can.Message, can.BusABC, ECUModel], None], arb_id: int):
        self.listener.remove_callback_for_id(rx_callback, arb_id)

    def start(self):
        if self.running:
            return
        self.running = True
        self.notifier.add_listener(self.listener)

    def stop(self):
        if not self.running:
            return
        self.notifier.stop()
        self.bus.shutdown()
