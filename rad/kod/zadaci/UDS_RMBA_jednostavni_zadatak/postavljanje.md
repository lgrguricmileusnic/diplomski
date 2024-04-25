Za pokretanje zadatka potrebni su moduli jezgre:
- can_gw
- can
- iso_tp

```bash
modprobe can_gw
modprobe can
modprobe can_isotp
```

Provjeriti s `lsmod | grep can`.

Zadatak kao i network driver plugin dostupni su na dockerhubu pa se postavljanje vrši kroz docker naredbe:

```bash
docker plugin install lovrogm/dockercan:latest
docker pull lovrogm/uds_ctf_task1:latest

docker network create -o centralised=false -o canfd=false -o host_if=dcan0 --driver lovrogm/dockercan:latest can
docker run --network can lovrogm/uds_ctf_task1:latest
```
