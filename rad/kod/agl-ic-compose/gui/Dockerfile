# Use the official Flutter image as a base
FROM cirrusci/flutter:latest

WORKDIR /app

COPY config.yaml /app/config.yaml
COPY api_key.txt /app/api_key.txt




ENTRYPOINT ["/app/entrypoint.sh"]
