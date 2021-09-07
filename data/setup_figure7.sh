#!/bin/bash
mkdir apps_fast && cd apps_fast

cp -r ${WD}/brotli-expanded brotli-decompressor
mv brotli-decompressor/src/lib.rs.unsafe brotli-decompressor/src/lib.rs

SHA=ba4bc6d7c35677a3731bd89f95ed9c9e2dac0c4b
wget https://github.com/tantivy-search/tantivy/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=85ad2b1f7d4c08f40f33f6925ae6cdccc3ec35b4
wget https://github.com/RustPython/RustPython/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=6e2595a191f2dd72a91a632e51b66b1cf5187083
wget https://github.com/getzola/zola/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=0daa7e2add76f7d40a63dad4f831f753d35504ce
wget https://github.com/wasmerio/wasmer/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=7382303182863a3f2ca575a3c421fdf4361885de
wget https://github.com/utah-scs/splinter/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

cd ..
mkdir apps_full && cd apps_full

cp -r ${WD}/brotli-expanded brotli-decompressor
mv brotli-decompressor/src/lib.rs.unsafe brotli-decompressor/src/lib.rs

SHA=be39ddaf7d5f017da9597a94f6fd66e17e7df2e3
wget https://github.com/gfx-rs/gfx/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=ba4bc6d7c35677a3731bd89f95ed9c9e2dac0c4b
wget https://github.com/tantivy-search/tantivy/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=b1d2a306ce5a017d249c050d904449f6895144dd
wget https://github.com/cloudflare/quiche/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=4a03710adcc7acee2c773a97d25ffd3de18efea9
wget https://github.com/seanmonstar/warp/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=173ba3cc30f99a63606988ecaee0017d643c9a1e
wget https://github.com/Schniz/fnm/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=d414206736070726bcbaecc51919f1931e9f17cf
wget https://github.com/hyperium/tonic/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=0c9b44108a0726ed28d7fa78965bbc97b2c0598c
wget https://github.com/timberio/vector/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=151900ba9645253fa8e1f780b5446d32fc30c4a5
wget https://github.com/google/flatbuffers/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=a367796e66eeac42d9ce1294c0fbbca6191e9cf3
wget https://github.com/firecracker-microvm/firecracker/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=00461f3a76ed82f41f334cd34008209563c473e5
wget https://github.com/swc-project/swc/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=b8bf28b38d3fdd13b497fb0da2b5baccb4670b81
wget https://github.com/valeriansaliou/sonic/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=0daa7e2add76f7d40a63dad4f831f753d35504ce
wget https://github.com/wasmerio/wasmer/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=6708ce171792df02e1e90e1fe1e67e424d1586c8
wget https://github.com/tikv/tikv/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=85ad2b1f7d4c08f40f33f6925ae6cdccc3ec35b4
wget https://github.com/RustPython/RustPython/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=177290d82aa5bb5d7376389e7de5c886986ed11d
wget https://github.com/diesel-rs/diesel/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=6e2595a191f2dd72a91a632e51b66b1cf5187083
wget https://github.com/getzola/zola/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=cde77e5e0e9bfa1bf1230f4bdd8491f4f4cdc72c
wget https://github.com/iron/iron/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=4aa52a2dbb5feed86dcafa3afe8d554975ca5518
wget https://github.com/str4d/rage/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=3d546aa57832875718ec95cffe7bcade727e617a
wget https://github.com/cloudflare/boringtun/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=4b7babbe99c04bd573aad49db24484d07c574ae9
wget https://github.com/BLAKE3-team/BLAKE3/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=91fabec6bef70b8714354843930ecee3c779219b
wget https://github.com/influxdata/flux/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=7382303182863a3f2ca575a3c421fdf4361885de
wget https://github.com/utah-scs/splinter/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=71dfb94beaeac107d7cd359985f9bd66fd223e1b
wget https://github.com/NetSys/NetBricks/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=19be2cd3fa4b8fe2560dda9a62f1c2271f9fb41e
wget https://github.com/servo/servo/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

SHA=f90389736b755ff0063b6abfeeeaedeaeec08acd
wget https://github.com/mozilla/gecko-dev/archive/${SHA}.tar.gz
tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

cd ../..
