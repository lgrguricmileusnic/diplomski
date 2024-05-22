FROM cirrusci/flutter:3.3.1 as builder

COPY ./gui/ /gui

WORKDIR /gui

RUN apt-get update -y && apt-get upgrade -y 
RUN apt-get install -y cmake

RUN flutter build linux --release


FROM ubuntu:latest

COPY --from=builder /gui/build/linux/x64/release/bundle/gui .
RUN apt-get install libgtk-3-0 libblkid1 liblzma5
