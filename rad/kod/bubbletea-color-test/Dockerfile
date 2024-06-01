FROM golang:1.22-alpine as builder
COPY . /ic-tui
WORKDIR /ic-tui
RUN go install
CMD ["bt-color-test"]

FROM ubuntu:latest
# RUN apk update && apk upgrade
COPY --from=builder /go/bin/bt-color-test .
EXPOSE 22/tcp
CMD ["/bt-color-test"]