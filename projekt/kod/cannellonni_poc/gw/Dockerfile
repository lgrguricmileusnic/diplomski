FROM alpine

RUN apk add bash can-utils git cmake build-base linux-headers

RUN git clone https://github.com/mguentner/cannelloni.git \
    && cd cannelloni \
    && cmake -DCMAKE_BUILD_TYPE=Release \
    && make \
    && make install \
    ;

COPY ./setup_gw.sh /
RUN chmod +x /setup_gw.sh

ENTRYPOINT ["/setup_gw.sh"]
