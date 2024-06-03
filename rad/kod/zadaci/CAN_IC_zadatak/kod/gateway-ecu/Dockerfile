FROM alpine
LABEL authors="Lovro Grgurić Mileusnić"

COPY ./ecu_template /ecu/ecu_template
COPY ./impl /ecu/impl
COPY ./*.py /ecu/
COPY ./requirements.txt /ecu

WORKDIR /ecu

RUN apk update
RUN apk add python3 py3-pip py3-virtualenv

RUN python3 -m venv venv

RUN venv/bin/pip3 install -r requirements.txt



ENTRYPOINT ["venv/bin/python3", "main.py"]