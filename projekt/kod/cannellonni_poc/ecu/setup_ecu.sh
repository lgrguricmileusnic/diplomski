#!/bin/bash
ip link add dev vcan0 type vcan
ip link set dev vcan0 up

echo "Set up vcan0"

/bin/bash