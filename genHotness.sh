#!/bin/bash

# Generate hotness with valgrind
script_path=`realpath $0`
root_path=`dirname $script_path`

valgrind --tool=callgrind --callgrind-out-file=callgrind.out $1 $2
perl $root_path/callgrind_get_unchecked_parser.perl --auto=yes callgrind.out > cal.out

