SRC_DIR=./cmd/
BUILD_DIR=./build/
SCRIPTS_DIR=./scripts/

PROG=ic-tui

build: ic-tui


ic-tui:
	go build -o ${BUILD_DIR}${PROG} ${SRC_DIR}


.PHONY: build ic-tui

clean:
	rm -fdr ./build
	go clean