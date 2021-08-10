#!/bin/bash
#mkdir apps_fast && cd apps_fast

#### Apps Fast ####

#cp -r ../../brotli-expanded brotli-decompressor
#mv brotli-decompressor/src/lib.rs.unsafe brotli-decompressor/src/lib.rs
#
#SHA=3bedb42b0b8ef06967eecaa63b8faa82dbe9cd00
#wget https://github.com/getzola/zola/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=f6cf6e889b1f8595dbd6b62f30c71562c1465d01
#wget https://github.com/tantivy-search/tantivy/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=b33f72eb4d329b7ad409ba454b0b800802294cbb
#wget https://github.com/RustPython/RustPython/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=a3a73d35e3ba4880a31009bfba6b10fe4dd812a9
#wget https://github.com/wasmerio/wasmer/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=7382303182863a3f2ca575a3c421fdf4361885de
#wget https://github.com/utah-scs/splinter/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

#cd ..
mkdir apps_full && cd apps_full

#### Apps Full ####

#cp -r ../../brotli-expanded brotli-decompressor
#mv brotli-decompressor/src/lib.rs.unsafe brotli-decompressor/src/lib.rs
#
#SHA=3bedb42b0b8ef06967eecaa63b8faa82dbe9cd00
#wget https://github.com/getzola/zola/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=f6cf6e889b1f8595dbd6b62f30c71562c1465d01
#wget https://github.com/tantivy-search/tantivy/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=b33f72eb4d329b7ad409ba454b0b800802294cbb
#wget https://github.com/RustPython/RustPython/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=a3a73d35e3ba4880a31009bfba6b10fe4dd812a9
#wget https://github.com/wasmerio/wasmer/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=fb4afce29d0a02620e0a5957f1892d83c665b5f8
##wget https://github.com/cloudflare/quiche/archive/${SHA}.tar.gz
##tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#git clone --recursive https://github.com/cloudflare/quiche
#cd quiche && git checkout ${SHA} && cd ..
#
#SHA=ffe49abb5626934fbcc807dbeb7824d437a53cd4
#wget https://github.com/seanmonstar/warp/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=fd584746a6206d4138f35966629c000026f5fe96
#wget https://github.com/Schniz/fnm/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=a7b527d9427485c9758a36e1ffdb148ac2b0124a
#wget https://github.com/google/flatbuffers/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=2c52021ed42adc8d3524562c21a0dfca31c8d110
#wget https://github.com/swc-project/swc/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=6844d6b289c9c05f60614b291428cf57a43d1c6e
#wget https://github.com/iron/iron/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=8d02ba25a9ec422d5d9f2d91a541b615f5e41c6e
#wget https://github.com/str4d/rage/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=f107b55cd7f73a2678738585685309c108e2fa51
#wget https://github.com/cloudflare/boringtun/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=4032a51a328a448f14a2aff000309980ccc8c968
#wget https://github.com/BLAKE3-team/BLAKE3/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#SHA=a4018dee82f767ebc53348811f413b7a13bab90c
#wget https://github.com/influxdata/flux/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

#SHA=0fec57c05d3996cc00c55a66f20dd5793a9bfb5d
#wget https://github.com/mozilla/gecko-dev/archive/${SHA}.tar.gz
#tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

## Cannot compile ##

# dependency error
SHA=bc77309afdb0829605982370a3e17382c5968071
wget https://github.com/gfx-rs/gfx/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

# proto buffers??
SHA=efe0865d26b7cfcb4b5755dc2b723d96a581dd95
wget https://github.com/hyperium/tonic/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

# no libclang?
SHA=53fe64d7487a166c822485a0e74422fd05c1f633
wget https://github.com/timberio/vector/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=b02f3bb083edcb60cf718722949196df2e915d05
wget https://github.com/valeriansaliou/sonic/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

# getting killed
SHA=5edc4ddf331f1e8420f856b6a5173383e3197569
wget https://github.com/tikv/tikv/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=3e56446dd5d1d4ee09a55ce9dbdaeb7776cfa8ca
wget https://github.com/servo/servo/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

# lazy-static (can't find std/core?)
SHA=366afed1bd0b5cb71e82a4f05d3e30a208fab88a
wget https://github.com/firecracker-microvm/firecracker/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

# need openssl
SHA=7382303182863a3f2ca575a3c421fdf4361885de
wget https://github.com/utah-scs/splinter/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

# misc
SHA=6e46d08d1a745dff513707cada690dac8246cf98
wget https://github.com/diesel-rs/diesel/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=71dfb94beaeac107d7cd359985f9bd66fd223e1b
wget https://github.com/NetSys/NetBricks/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

cd ../..
