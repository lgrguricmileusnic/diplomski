# see https://scapy.readthedocs.io/en/latest/layers/automotive.html#native-cansocket
CAN_FILTERS = [
    {"can_id": 0x456, "can_mask": 0x7FF},
]

# receive and transmit arbitration IDs (ISO-TP address of the UDS server)
UDS = dict(rx_id=0x100, tx_id=0x101)

XCP = [
    {"can_id": 0x701, "can_mask": 0x7FF},
]
