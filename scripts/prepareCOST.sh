#!/bin/bash

script_path=`realpath $0`
COST_ROOT=`dirname $script_path`/../COST
BMARK_ROOT=`dirname $script_path`/../benchmarks

cd $COST_ROOT
rm -rf vendor-safe vendor-unsafe vendor
cp $BMARK_ROOT/patch/COST.Cargo.lock Cargo.lock
cp $BMARK_ROOT/patch/COST.Cargo.toml Cargo.toml
cp $BMARK_ROOT/patch/COST.pagerank.rs src/bin/pagerank.rs
cp $BMARK_ROOT/patch/COST.lib.rs src/lib.rs
cp $BMARK_ROOT/patch/COST.bench.rs src/bench.rs

cargo vendor >> log_vendor 2>&1
mv vendor vendor-safe
cp -r vendor-safe vendor-unsafe
ln -sf $BMARK_ROOT/../scripts/regexify.py .; ln -sf $BMARK_ROOT/make_patch.py .
rm -f vendor; ln -s vendor-safe vendor; python3 make_patch.py -t $(pwd) -r vendor >> log 2>&1

# Gen unsafe binary
rm -f vendor; ln -s vendor-unsafe vendor

