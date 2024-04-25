import argparse

import impl.config as config
from ecu_template.ecu import ECU
from impl.can_handler import CanHandlerImpl
from impl.ecu_model import ECUModelImpl
from impl.uds_handler import UDSHandlerImpl


def loop(_ecu: ECU):
    _ecu.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down...")
        _ecu.stop()


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("interface", default="ccan_0", type=str, nargs="?")
    argparser.add_argument("canfd", default=False, type=bool, nargs="?")
    args = argparser.parse_args()

    ecu_model = ECUModelImpl()
    ecu = ECU(
        interface=args.interface,
        canfd=args.canfd,
        can_handler=CanHandlerImpl(ecu_model),
        uds_handler=UDSHandlerImpl(ecu_model),
        uds_config=config.UDS,
        can_filters=config.CAN_FILTERS,
    )

    loop(ecu)


if __name__ == "__main__":
    main()
