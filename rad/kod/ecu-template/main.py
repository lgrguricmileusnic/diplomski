import argparse
import ecu_template.callbacks.can_raw as can_raw
from ecu_template.ecu import ECU

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("interface", default="vcan0", type=str, nargs="?")
    args = argparser.parse_args()

    ecu1 = ECU(interface="vcan0")
    ecu1.can_controller.add_callback_for_id(can_raw.echo, 0x123)
    ecu1.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        ecu1.stop()
