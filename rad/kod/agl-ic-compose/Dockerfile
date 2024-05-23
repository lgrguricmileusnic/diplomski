FROM ghcr.io/cirruslabs/flutter:3.7.12 as builder

RUN apt-get update -y && apt-get upgrade -y 
RUN apt-get install -y \
      curl git unzip \
      xz-utils zip libglu1-mesa \
      clang cmake git \
      ninja-build pkg-config \
      libgtk-3-dev liblzma-dev \
      libstdc++-12-dev

COPY ./gui/ /gui
WORKDIR /gui

RUN flutter doctor
RUN dart --version
RUN flutter pub get
RUN flutter create --platforms=linux .
RUN flutter build linux --release

RUN ls -lah build/linux/x64/release/bundle/lib


FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y libgtk-3-0 libblkid1 liblzma5

RUN 	apt-get install -qqy x11-apps x11vnc xvfb
# RUN     mkdir ~/.vnc 
# RUN     x11vnc -storepasswd 1234 ~/.vnc/passwd 
COPY --from=builder /gui/build/linux/x64/release/bundle/ agl-ic
RUN export LIBGL_ALWAYS_SOFTWARE=1

ENTRYPOINT ["/agl-ic/gui"]
# ENTRYPOINT ["/bin/bash"]