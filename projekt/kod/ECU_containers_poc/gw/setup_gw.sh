#!/bin/bash
nbuses=3

echo "Setting up can gateway..."
for i in $(seq 1 $nbuses)
do
    ip link add dev vcan$i type vcan
    ip link set dev vcan$i up
done

echo "Setup done"

/bin/bash
