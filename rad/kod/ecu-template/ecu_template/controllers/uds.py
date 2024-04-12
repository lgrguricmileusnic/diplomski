import can
import isotp
from typing import Callable
from ..models.ecu_model import ECUModel
from .controller import Controller


class UDSController(Controller):

    def __init__(self, bus: can.BusABC, model: ECUModel):
        self.bus = bus
        self.notifier = can.Notifier(self.bus, [])
        self.transport_layer = isotp.NotifierBasedCanStack(self.bus, self.notifier)
        self.ecu = model
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        # starts notifier
        self.transport_layer.start()

    def stop(self):
        if not self.running:
            return
        self.transport_layer.stop()
        self.notifier.stop()
