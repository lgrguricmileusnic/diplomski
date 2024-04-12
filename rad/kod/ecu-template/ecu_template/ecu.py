import can
from .controllers.can_raw import CanController
from .controllers.uds import UDSController
from .models.ecu_model import ECUModel


class ECU:
    def __init__(self, interface: str):
        self._bus = can.Bus(interface, "socketcan", ignore_config=True)
        self._ecu = ECUModel()
        self.can_controller = CanController(self._bus, self._ecu)
        self.uds_controller = UDSController(self._bus, self._ecu)

    def start(self):
        self.can_controller.start()

    def stop(self):
        self.can_controller.stop()
