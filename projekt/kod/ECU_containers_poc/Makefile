build:
	docker compose build
run:
	docker compose up -d
	./setup_vxcan.sh ecu_containers_poc-gw-1 ecu_containers_poc-ecu{1..5}-1 

kill:
	docker compose down
