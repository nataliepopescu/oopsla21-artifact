FROM ubuntu
ENV ROOT=/root
SHELL ["/bin/bash", "-c"]

# Squash timezone promting
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update && apt-get -y install git \
    curl \
    wget \
    python3-pip \
    libssl-dev \
    unzip \
    pkg-config \
    vim

RUN pip3 install numpy==1.20.1
RUN pip3 install dash==1.13.4
RUN pip3 install Brotli==1.0.9
RUN pip3 install tqdm
RUN pip3 install scipy

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y
ENV PATH="~/.cargo/bin:${PATH}"

# Install cargo-edit
ENV OPENSSL_DIR="/usr/bin/openssl"
ENV OPENSSL_LIB_DIR="/usr/lib/x86_64-linux-gnu"
ENV OPENSSL_INCLUDE_DIR="/usr/include/openssl"
RUN cargo install cargo-edit

# Copy over artifact dir
WORKDIR ${ROOT}
ENV NADER=nader
RUN mkdir ${NADER}
WORKDIR ${ROOT}/${NADER}
COPY . .

##### Figure 1 Setup #####
ENV F1=figure1
ENV CRATES_FAST=crates_fast
ENV CRATES_FULL=crates_full
WORKDIR ${ROOT}/${NADER}/${F1}
RUN mkdir ${CRATES_FAST}
RUN mkdir ${CRATES_FULL}

# for euc
RUN apt-get install -y libxkbcommon-dev
ENV PKG_CONFIG_PATH="/usr/lib/x86_64-linux-gnu/pkgconfig"

# Fast run
WORKDIR ${ROOT}/${NADER}/${F1}/${CRATES_FAST}

RUN wget www.crates.io/api/v1/crates/prost/0.7.0/download
RUN tar -xzf download && rm download
COPY ./locks/prost-0.7.0_Cargo.lock prost-0.7.0/Cargo.lock

# Full run
WORKDIR ${ROOT}/${NADER}/${F1}/${CRATES_FULL}

RUN wget www.crates.io/api/v1/crates/combine/4.5.2/download
RUN tar -xzf download && rm download
COPY ./locks/combine-4.5.2_Cargo.lock combine-4.5.2/Cargo.lock

RUN wget www.crates.io/api/v1/crates/string-interner/0.12.2/download
RUN tar -xzf download && rm download
COPY ./locks/string-interner-0.12.2_Cargo.lock string-interner-0.12.2/Cargo.lock

RUN wget www.crates.io/api/v1/crates/prost/0.7.0/download
RUN tar -xzf download && rm download
COPY ./locks/prost-0.7.0_Cargo.lock prost-0.7.0/Cargo.lock

RUN wget www.crates.io/api/v1/crates/glam/0.14.0/download
RUN tar -xzf download && rm download
COPY ./locks/glam-0.14.0_Cargo.lock glam-0.14.0/Cargo.lock

RUN wget www.crates.io/api/v1/crates/primal-sieve/0.3.1/download
RUN tar -xzf download && rm download
COPY ./locks/primal-sieve-0.3.1_Cargo.lock primal-sieve-0.3.1/Cargo.lock

RUN wget www.crates.io/api/v1/crates/euc/0.5.3/download
RUN tar -xzf download && rm download
COPY ./locks/euc-0.5.3_Cargo.lock euc-0.5.3/Cargo.lock

RUN wget www.crates.io/api/v1/crates/roaring/0.6.5/download
RUN tar -xzf download && rm download
COPY ./locks/roaring-0.6.5_Cargo.lock roaring-0.6.5/Cargo.lock

##### Figure 7 Setup #####
ENV F7=figure7
ENV APPS_FAST=apps_fast
ENV APPS_FULL=apps_full
WORKDIR ${ROOT}/${NADER}/${F7}
RUN mkdir ${APPS_FAST}
RUN mkdir ${APPS_FULL}

# Quick run
WORKDIR ${ROOT}/${NADER}/${F7}/${APPS_FAST}

RUN cp -r ${ROOT}/${NADER}/brotli-expanded brotli-decompressor
RUN mv brotli-decompressor/src/lib.rs.unsafe brotli-decompressor/src/lib.rs

ENV SHA=ba4bc6d7c35677a3731bd89f95ed9c9e2dac0c4b
RUN wget https://github.com/tantivy-search/tantivy/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=85ad2b1f7d4c08f40f33f6925ae6cdccc3ec35b4
RUN wget https://github.com/RustPython/RustPython/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=6e2595a191f2dd72a91a632e51b66b1cf5187083
RUN wget https://github.com/getzola/zola/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=0daa7e2add76f7d40a63dad4f831f753d35504ce
RUN wget https://github.com/wasmerio/wasmer/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

ENV SHA=7382303182863a3f2ca575a3c421fdf4361885de
RUN wget https://github.com/utah-scs/splinter/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

# Full run
#WORKDIR ${ROOT}/${NADER}/${F7}/${APPS_FULL}
#
#RUN cp -r ${ROOT}/${NADER}/brotli-expanded brotli-decompressor
#RUN mv brotli-decompressor/src/lib.rs.unsafe brotli-decompressor/src/lib.rs
#
#ENV SHA=be39ddaf7d5f017da9597a94f6fd66e17e7df2e3
#RUN wget https://github.com/gfx-rs/gfx/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=ba4bc6d7c35677a3731bd89f95ed9c9e2dac0c4b
#RUN wget https://github.com/tantivy-search/tantivy/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=b1d2a306ce5a017d249c050d904449f6895144dd
#RUN wget https://github.com/cloudflare/quiche/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=4a03710adcc7acee2c773a97d25ffd3de18efea9
#RUN wget https://github.com/seanmonstar/warp/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=173ba3cc30f99a63606988ecaee0017d643c9a1e
#RUN wget https://github.com/Schniz/fnm/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=d414206736070726bcbaecc51919f1931e9f17cf
#RUN wget https://github.com/hyperium/tonic/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=0c9b44108a0726ed28d7fa78965bbc97b2c0598c
#RUN wget https://github.com/timberio/vector/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=151900ba9645253fa8e1f780b5446d32fc30c4a5
#RUN wget https://github.com/google/flatbuffers/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=a367796e66eeac42d9ce1294c0fbbca6191e9cf3
#RUN wget https://github.com/firecracker-microvm/firecracker/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=00461f3a76ed82f41f334cd34008209563c473e5
#RUN wget https://github.com/swc-project/swc/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=b8bf28b38d3fdd13b497fb0da2b5baccb4670b81
#RUN wget https://github.com/valeriansaliou/sonic/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=0daa7e2add76f7d40a63dad4f831f753d35504ce
#RUN wget https://github.com/wasmerio/wasmer/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=6708ce171792df02e1e90e1fe1e67e424d1586c8
#RUN wget https://github.com/tikv/tikv/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=85ad2b1f7d4c08f40f33f6925ae6cdccc3ec35b4
#RUN wget https://github.com/RustPython/RustPython/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=177290d82aa5bb5d7376389e7de5c886986ed11d
#RUN wget https://github.com/diesel-rs/diesel/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=6e2595a191f2dd72a91a632e51b66b1cf5187083
#RUN wget https://github.com/getzola/zola/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=cde77e5e0e9bfa1bf1230f4bdd8491f4f4cdc72c
#RUN wget https://github.com/iron/iron/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=4aa52a2dbb5feed86dcafa3afe8d554975ca5518
#RUN wget https://github.com/str4d/rage/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=3d546aa57832875718ec95cffe7bcade727e617a
#RUN wget https://github.com/cloudflare/boringtun/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=4b7babbe99c04bd573aad49db24484d07c574ae9
#RUN wget https://github.com/BLAKE3-team/BLAKE3/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=91fabec6bef70b8714354843930ecee3c779219b
#RUN wget https://github.com/influxdata/flux/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=7382303182863a3f2ca575a3c421fdf4361885de
#RUN wget https://github.com/utah-scs/splinter/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=71dfb94beaeac107d7cd359985f9bd66fd223e1b
#RUN wget https://github.com/NetSys/NetBricks/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=19be2cd3fa4b8fe2560dda9a62f1c2271f9fb41e
#RUN wget https://github.com/servo/servo/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
#
#ENV SHA=f90389736b755ff0063b6abfeeeaedeaeec08acd
#RUN wget https://github.com/mozilla/gecko-dev/archive/${SHA}.tar.gz
#RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz

# For orca (dumping figures)
WORKDIR ${ROOT}

RUN apt-get -y install xvfb \
    libgtk2.0-0 \
    libxtst6 \
    libxss1 \
    libgconf-2-4 \
    libnss3

RUN wget https://github.com/plotly/orca/releases/download/v1.1.1/orca-1.1.1-x86_64.AppImage
RUN chmod 777 orca-1.1.1-x86_64.AppImage

RUN ./orca-1.1.1-x86_64.AppImage --appimage-extract
RUN rm orca-1.1.1-x86_64.AppImage
RUN printf '#!/bin/bash \nxvfb-run --auto-servernum --server-args "-screen 0 640x480x24" ~/squashfs-root/app/orca "$@"' > /usr/bin/orca

RUN chmod 777 /usr/bin/orca
RUN chmod -R 777 squashfs-root/

##### Table 4 Setup #####
WORKDIR ${ROOT}/${NADER}
ENV SHA=a211dd5a7050b1f9e8a9870b95513060e72ac4a0
RUN wget https://github.com/wg/wrk/archive/${SHA}.tar.gz
RUN tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
WORKDIR ${ROOT}/${NADER}/wrk-${SHA}
RUN make
RUN mv wrk ${ROOT}/${NADER}/benchmarks
WORKDIR ${ROOT}/${NADER}
RUN rm -rf wrk-${SHA}

WORKDIR ${ROOT}/${NADER}
