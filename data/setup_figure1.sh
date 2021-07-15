#!/bin/bash
cd figure1
mkdir crates_fast && cd crates_fast

wget www.crates.io/api/v1/crates/prost/0.7.0/download
tar -xzf download && rm download
cp ../../locks/prost-0.7.0_Cargo.lock prost-0.7.0/Cargo.lock

cd ..
mkdir crates_full && cd crates_full

wget www.crates.io/api/v1/crates/combine/4.5.2/download
tar -xzf download && rm download
cp ../../locks/combine-4.5.2_Cargo.lock combine-4.5.2/Cargo.lock

wget www.crates.io/api/v1/crates/string-interner/0.12.2/download
tar -xzf download && rm download
cp ../../locks/string-interner-0.12.2_Cargo.lock string-interner-0.12.2/Cargo.lock

wget www.crates.io/api/v1/crates/prost/0.7.0/download
tar -xzf download && rm download
cp ../../locks/prost-0.7.0_Cargo.lock prost-0.7.0/Cargo.lock

wget www.crates.io/api/v1/crates/glam/0.14.0/download
tar -xzf download && rm download
cp ../../locks/glam-0.14.0_Cargo.lock glam-0.14.0/Cargo.lock

wget www.crates.io/api/v1/crates/primal-sieve/0.3.1/download
tar -xzf download && rm download
cp ../../locks/primal-sieve-0.3.1_Cargo.lock primal-sieve-0.3.1/Cargo.lock

wget www.crates.io/api/v1/crates/euc/0.5.3/download
tar -xzf download && rm download
cp ../../locks/euc-0.5.3_Cargo.lock euc-0.5.3/Cargo.lock

wget www.crates.io/api/v1/crates/roaring/0.6.5/download
tar -xzf download && rm download
cp ../../locks/roaring-0.6.5_Cargo.lock roaring-0.6.5/Cargo.lock

cd ..
