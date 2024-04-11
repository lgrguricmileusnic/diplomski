# File for implementing user defined callbacks
import can

def echo(msg: can.Message):
    with can.Bus("vcan0", "socketcan", ignore_config=True) as bus:
        # Increment arbitration ID to prevent callback infinite loop 
        msg.arbitration_id += 1
        bus.send(msg)