FROM ubuntu
ENV ROOT=/root
SHELL ["/bin/bash", "-c"]
RUN apt-get update
#RUN apt-get -y install cmake
RUN apt-get -y install git
RUN apt-get -y install curl
RUN apt-get -y install wget
RUN apt-get -y install python3-pip
RUN apt-get -y install libssl-dev
RUN pip3 install numpy
RUN pip3 install dash
RUN pip3 install pandas
RUN pip3 install Brotli

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y
ENV PATH="~/.cargo/bin:${PATH}"

# Install cargo-edit
ENV OPENSSL_DIR="/usr/bin/openssl"
ENV OPENSSL_LIB_DIR="/usr/lib/x86_64-linux-gnu"
ENV OPENSSL_INCLUDE_DIR="/usr/include/openssl"
RUN cargo install cargo-edit

# Set up benchmarking framework
WORKDIR ${ROOT}
RUN git clone https://github.com/nataliepopescu/bencher_scrape.git
WORKDIR ${ROOT}/bencher_scrape

# Download libraries for Figure 1
ENV F1=fig1
RUN mkdir ${F1}
WORKDIR ${ROOT}/bencher_scrape/${F1}

RUN wget www.crates.io/api/v1/crates/combine/4.5.2/download
RUN tar -xzf download && rm download
RUN wget www.crates.io/api/v1/crates/string-interner/0.12.2/download
RUN tar -xzf download && rm download
RUN wget www.crates.io/api/v1/crates/prost/0.7.0/download
RUN tar -xzf download && rm download
RUN wget www.crates.io/api/v1/crates/glam/0.14.0/download
RUN tar -xzf download && rm download
RUN wget www.crates.io/api/v1/crates/primal-sieve/0.3.1/download
RUN tar -xzf download && rm download
RUN wget www.crates.io/api/v1/crates/euc/0.5.3/download
RUN tar -xzf download && rm download
RUN wget www.crates.io/api/v1/crates/roaring/0.6.5/download
RUN tar -xzf download && rm download
WORKDIR ${ROOT}/bencher_scrape

# Download applications for Figure 7
ENV F7=fig7
RUN mkdir ${F7}
WORKDIR ${ROOT}/bencher_scrape/${F7}

ENV SHA=965cd00b2f971518f7326e12f317ba893eae3a6e
RUN wget https://github.com/dropbox/rust-brotli-decompressor/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=be39ddaf7d5f017da9597a94f6fd66e17e7df2e3
RUN wget https://github.com/gfx-rs/gfx/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=ba4bc6d7c35677a3731bd89f95ed9c9e2dac0c4b
RUN wget https://github.com/tantivy-search/tantivy/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=b1d2a306ce5a017d249c050d904449f6895144dd
RUN wget https://github.com/cloudflare/quiche/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=4a03710adcc7acee2c773a97d25ffd3de18efea9
RUN wget https://github.com/seanmonstar/warp/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=173ba3cc30f99a63606988ecaee0017d643c9a1e
RUN wget https://github.com/Schniz/fnm/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=d414206736070726bcbaecc51919f1931e9f17cf
RUN wget https://github.com/hyperium/tonic/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=0c9b44108a0726ed28d7fa78965bbc97b2c0598c
RUN wget https://github.com/timberio/vector/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=151900ba9645253fa8e1f780b5446d32fc30c4a5
RUN wget https://github.com/google/flatbuffers/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=a367796e66eeac42d9ce1294c0fbbca6191e9cf3
RUN wget https://github.com/firecracker-microvm/firecracker/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=00461f3a76ed82f41f334cd34008209563c473e5
RUN wget https://github.com/swc-project/swc/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=b8bf28b38d3fdd13b497fb0da2b5baccb4670b81
RUN wget https://github.com/valeriansaliou/sonic/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=0daa7e2add76f7d40a63dad4f831f753d35504ce
RUN wget https://github.com/wasmerio/wasmer/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=6708ce171792df02e1e90e1fe1e67e424d1586c8
RUN wget https://github.com/tikv/tikv/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=85ad2b1f7d4c08f40f33f6925ae6cdccc3ec35b4
RUN wget https://github.com/RustPython/RustPython/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=177290d82aa5bb5d7376389e7de5c886986ed11d
RUN wget https://github.com/diesel-rs/diesel/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=6e2595a191f2dd72a91a632e51b66b1cf5187083
RUN wget https://github.com/getzola/zola/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=cde77e5e0e9bfa1bf1230f4bdd8491f4f4cdc72c
RUN wget https://github.com/iron/iron/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=4aa52a2dbb5feed86dcafa3afe8d554975ca5518
RUN wget https://github.com/str4d/rage/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=3d546aa57832875718ec95cffe7bcade727e617a
RUN wget https://github.com/cloudflare/boringtun/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=4b7babbe99c04bd573aad49db24484d07c574ae9
RUN wget https://github.com/BLAKE3-team/BLAKE3/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=91fabec6bef70b8714354843930ecee3c779219b
RUN wget https://github.com/influxdata/flux/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=7382303182863a3f2ca575a3c421fdf4361885de
RUN wget https://github.com/utah-scs/splinter/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=71dfb94beaeac107d7cd359985f9bd66fd223e1b
RUN wget https://github.com/NetSys/NetBricks/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=19be2cd3fa4b8fe2560dda9a62f1c2271f9fb41e
RUN wget https://github.com/servo/servo/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

#ENV SHA=f90389736b755ff0063b6abfeeeaedeaeec08acd
#RUN wget https://github.com/mozilla/gecko-dev/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

WORKDIR ${ROOT}/bencher_scrape

# Setup for Figures 5 and 9
WORKDIR ${ROOT}
ENV NADER=nader
RUN mkdir ${NADER}
WORKDIR ${ROOT}/${NADER}
COPY . .
