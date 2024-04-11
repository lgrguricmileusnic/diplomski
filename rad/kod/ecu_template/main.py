import argparse
import ecu.callbacks.can_raw as can_raw
from ecu import ecu

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("interface", default="vcan0", type=str, nargs="?")
    args = argparser.parse_args()

    ecu1 = ecu.CANController(args.interface)
    ecu1.raw_can_handler.add_callback_for_id(can_raw.echo, 0x123)
    ecu1.start()
    try:
        while(True):
            pass
    except KeyboardInterrupt:
        ecu.stop()