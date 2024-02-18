vxcans=$(ip a | grep vcan | cut -d "@" -f 1 | cut -d " " -f 2 | sort | uniq -w 12 |tr -s "\n" " ")
vcans=$(ip a | grep can_host| cut -d ":" -f 2 | tr -d " ")
ifs="$vxcans $vcans"
echo $ifs

for i in $ifs; 
do
	sudo ip link delete $i;
done;


