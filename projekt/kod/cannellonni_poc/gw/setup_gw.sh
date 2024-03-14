#!/bin/bash
nbuses=3

echo "Setting up can gateway..."
for i in $(seq 1 $nbuses)
do
    ip link add dev vcan$i type vcan
    ip link set dev vcan$i up
done

cannelloni/cannelloni -I vcan1 -C s -R ecu1 -r 10001 -l 10001 -f
cannelloni/cannelloni -I vcan2 -C s -R ecu2 -r 10002 -l 10002 -f

echo "Setup done"

/bin/bash
