FROM alpine
RUN apk add bash && apk add can-utils
COPY ./setup_gw.sh /
RUN chmod +x /setup_gw.sh
ENTRYPOINT ["/setup_gw.sh"]
