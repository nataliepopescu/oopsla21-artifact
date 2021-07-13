#!/bin/bash

# Generate hotness with valgrind
script_path=`realpath $0`
root_path=`dirname $script_path`

cargo_root=`pwd`/
rm -rf target
RUSTFLAGS="-g" cargo build --jobs 1 --bin $1 > log 2>&1
cp target/debug/$1 exp.exe
rm -rf target

mkdir -p baseline/exp-genHotness
cd baseline/exp-genHotness
mv ../../exp.exe .

valgrind --tool=callgrind --callgrind-out-file=callgrind.out ./exp.exe $2
perl $root_path/callgrind_get_unchecked_parser.perl --auto=yes callgrind.out > cal.out
python3 $root_path/CleanUpCal.py $cargo_root

