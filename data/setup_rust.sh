#!/bin/bash

SHA=163068cb6f8998031925dc36eb31badb1683ca8f
git clone https://github.com/nataliepopescu/rust.git
cp config.toml rust/ && cd rust
git checkout ${SHA}
python3 x.py build && python3 x.py install
cd ../..
rustup toolchain link rust-mir-mod data/rust/build/x86_64-unknown-linux-gnu/stage2
rustup override set rust-mir-mod
