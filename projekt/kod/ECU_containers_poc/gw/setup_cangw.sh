#!/bin/bash

cangw -A -s gw_vxcan1 -d vcan1 -X -e
cangw -A -s vcan1 -d gw_vxcan1 -X -e
cangw -A -s vcan1 -d gw_vxcan2 -X -e
cangw -A -s gw_vxcan2 -d vcan1 -X -e
