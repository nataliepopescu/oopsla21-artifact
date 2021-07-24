#!/bin/bash

iron/hello-$1 &
sleep 2
./wrk --latency -t12 -c100 -d30s http://localhost:3030/
