#!/bin/bash

./hello-$1 &
pid=$!
sleep 2
../wrk --latency -t12 -c100 -d30s http://localhost:3000/
kill -9 $pid
