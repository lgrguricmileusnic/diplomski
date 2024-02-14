FROM alpine
RUN apk add bash && apk add can-utils

COPY ./setup_ecu.sh /
COPY ./setup_cangw.sh /
RUN chmod +x /setup_ecu.sh
RUN chmod +x /setup_cangw.sh
ENTRYPOINT ["/setup_ecu.sh"]
