#!/bin/bash

# Run the experiment on a specific core (processor #1, not #0); this further 
# reduce variance of the results
#
# Usage: ./runExp.sh exp.exe [$ARGS]

# core #1
echo time taskset 0x00000002 nice -n 20 $1 $2
time taskset 0x00000002 nice -n -20 $1 $2  #| grep "ns/iter"
