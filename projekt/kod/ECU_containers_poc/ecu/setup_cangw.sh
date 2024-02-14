#!/bin/bash

cangw -A -s vcan0 -d ecu_vxcan -X -e -i
cangw -A -s ecu_vxcan -d vcan0 -X -e -i


# cangw -A -s vcan0 -d ecu_vxcan -X -e
# cangw -A -s ecu_vxcan -d vcan0 -X -e 