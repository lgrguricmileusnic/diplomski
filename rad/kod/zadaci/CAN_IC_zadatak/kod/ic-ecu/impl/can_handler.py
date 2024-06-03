from scapy.layers.can import CAN

from ecu_template.handler.can.can_handler import CanHandler
from impl.ecu_model import ECUModelImpl


class SpeedData:
    def __init__(self, data: bytes):
        self.speed = int.from_bytes(data[1:3])


class DashData:
    def __init__(self, data: bytes):
        """
        Init
        :param data: data from CAN packet
        """

        """
        Status register
        2 MSB not used
        6 LSB used as BELT, ENG, BAT, DOOR, OIL, BLINKER status        
        """
        status = data[1]
        self.blinkers = bool(status & 1)
        self.oil = bool(status & 2)
        self.door = bool(status & 4)
        self.bat = bool(status & 8)
        self.engine = bool(status & 16)
        self.belt = bool(status & 32)


class CanHandlerImpl(CanHandler):
    def __init__(self, ecu: ECUModelImpl):
        super().__init__(ecu)

    def handle_msg(self, msg: CAN):
        if msg.data[0] == 0xAB and msg.length == 3:
            speed_data = SpeedData(data=msg.data)
            if 0 < speed_data.speed <= 250:
                self.ecu.set_speed(speed_data.speed)
        elif msg.data[0] == 0xBB and msg.length == 2:
            dash_data = DashData(data=msg.data)
            self.ecu.set_dash(
                dash_data.belt,
                dash_data.engine,
                dash_data.bat,
                dash_data.door,
                dash_data.oil,
                dash_data.blinkers,
            )
