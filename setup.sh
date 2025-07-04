#!/bin/bash
    echo "START: Building Naabu"
    apt update
    apt install -y build-essential ca-certificates wget unzip git
    apt install -y python3 python3-pip python-is-python3
    wget https://go.dev/dl/go1.24.4.linux-amd64.tar.gz && tar -C /usr/local -xzf go1.24.4.linux-amd64.tar.gz && rm go1.24.4.linux-amd64.tar.gz
    export GOROOT=/usr/local/go
    export GOPATH=/go
    export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
    export GO111MODULE=on
    export CGO_ENABLED=1
    mkdir -p /go/src
    mkdir -p /go/bin
    cd /tmp && go install -v github.com/projectdiscovery/naabu/cmd/naabu@latest && cd -
    echo "END: Building Naabu"