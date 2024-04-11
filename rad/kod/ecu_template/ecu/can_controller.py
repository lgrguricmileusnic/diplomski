
import ecu.handlers.can_raw as can_raw


class CANController():    
    def __init__(self, interface: str):
        self.raw_can_handler = can_raw.RawCanHandler(interface)
    def start(self):
        self.raw_can_handler.start()
    def stop(self):
        self.raw_can_handler.stop()

