#!/bin/bash

Help ()
{
    echo "usage: setup_vxcan.sh <gw_container> <ecu_container_1> ... <ecu_container_n>"
}

if [[ $# -lt 2 ]]; then
    Help
    exit 1
fi

gw=$1
gw_id=`docker inspect -f '{{ .State.Pid }}' $gw`
echo "Gateway id: $gw_id"
ecus="${@:2}"
ecu_ids=()
for ecu in $ecus
do
    ecu_id=`docker inspect -f '{{ .State.Pid }}' $ecu`
    ecu_ids+=($ecu_id)
done

echo "ECU ids: ${ecu_ids[@]}"

i=1
for ecu_id in ${ecu_ids[@]}
do
    echo "Setting up vxcan pair gw_vxcan$i ecu_vxcan for ecu with ID $ecu_id" 
    sudo -- sh -c "
        ip link add gw_vxcan$i type vxcan peer name ecu_vxcan
        ip link set ecu_vxcan netns $ecu_id
        ip link set gw_vxcan$i netns $gw_id
        sudo nsenter -t $ecu_id -n ip link set ecu_vxcan up
        sudo nsenter -t $gw_id -n ip link set gw_vxcan$i up
    "

    
    i=$((i+1))
done
