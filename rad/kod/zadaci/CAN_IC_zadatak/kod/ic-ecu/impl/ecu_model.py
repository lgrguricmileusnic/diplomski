import json

import requests

from ecu_template.model.ecu_model import ECUModel
from ecu_template.model.listener.listener import Listener


class ECUModelImpl(ECUModel):
    def __init__(self):
        super().__init__()
        self.speed = 0.0
        self.blinkers = False
        self.belt = True
        self.engine = False
        self.bat = False
        self.door = False
        self.oil = False
        self.win_condition = True
        self.notify()

    def set_speed(self, speed: float):
        self.speed = speed
        self.check_and_update_win_condition()
        self.notify()

    def set_blinkers(self, blinkers: bool):
        self.blinkers = blinkers
        self.check_and_update_win_condition()
        self.notify()

    def check_and_update_win_condition(self):
        if self.speed > 230.0 and self.blinkers:
            self.win_condition = True


class IC_Listener(Listener):
    def update(self, model: ECUModelImpl):
        data = json.dumps(
            {
                "winCondition": model.win_condition,
                "speed": model.speed,
                "blinkers": model.blinkers,
                "seatbelt": model.belt,
                "engine": model.engine,
                "battery": model.bat,
                "doors": model.door,
                "oil": model.oil,
            }
        ).encode()
        requests.post("ic:8080", data=data)


def setup_ecu_model():
    model = ECUModelImpl()
    model.attach_listener(IC_Listener())
    return model
