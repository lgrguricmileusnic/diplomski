# File for implementing user defined callbacks
import can
from ecu_template.models.ecu_model import ECUModel


def echo(msg: can.Message, bus: can.BusABC, model: ECUModel):
    # Increment arbitration ID to prevent callback infinite loop
    msg.arbitration_id += 1
    bus.send(msg)
