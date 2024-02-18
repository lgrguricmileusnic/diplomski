#!/bin/bash

# cangw -A -s gw_vxcan1 -d vcan1 -X -e
# cangw -A -s vcan1 -d gw_vxcan1 -X -e
# cangw -A -s vcan1 -d gw_vxcan2 -X -e
# cangw -A -s gw_vxcan2 -d vcan1 -X -e

# cangw -A -s gw_vxcan1 -d vcan1 -X -e -i
# cangw -A -s vcan1 -d gw_vxcan1 -X -e -i
# cangw -A -s vcan1 -d gw_vxcan2 -X -e -i
# cangw -A -s gw_vxcan2 -d vcan1 -X -e -i

cangw -A -s vcan1 -d vcan2 -X -e # 0 handled 0 dropped 15 deleted
cangw -A -s vcan2 -d vcan1 -X -e # 78 handled 0 dropped 0 deleted
cangw -A -s vcan2 -d gw_vxcan4 -X -e # 78 handled 0 dropped 0 deleted
cangw -A -s gw_vxcan4 -d vcan2 -X -e # 15 handled 0 dropped 15 deleted
cangw -A -s gw_vxcan3 -d vcan1 -X -e # 0 handled 0 dropped 63 deleted
cangw -A -s vcan1 -d gw_vxcan3 -X -e # 75 handled 0 dropped 15 deleted
cangw -A -s gw_vxcan2 -d vcan1 -X -e # 0 handled 0 dropped 102 deleted
cangw -A -s vcan1 -d gw_vxcan2 -X -e # 126 handled 0 dropped 15 deleted
cangw -A -s vcan1 -d gw_vxcan1 -X -e # 126 handled 0 dropped 15 deleted
cangw -A -s gw_vxcan1 -d vcan1 -X -e # 39 handled 0 dropped 102 deleted
