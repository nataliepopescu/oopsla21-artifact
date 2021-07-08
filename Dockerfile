FROM ubuntu
ENV WD=/root
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

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y
ENV PATH="~/.cargo/bin:${PATH}"
ENV OPENSSL_DIR="/usr/bin/openssl"
ENV OPENSSL_LIB_DIR="/usr/lib/x86_64-linux-gnu"
ENV OPENSSL_INCLUDE_DIR="/usr/include/openssl"
RUN cargo install cargo-edit

# Set up benchmarking framework
WORKDIR ${WD}
RUN git clone https://github.com/nataliepopescu/bencher_scrape.git
WORKDIR ${WD}/bencher_scrape

# Download libraries for Figure 1
ENV F1=fig1
RUN mkdir ${F1}
WORKDIR ${WD}/bencher_scrape/${F1}
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
WORKDIR ${WD}/bencher_scrape

# Download applications for Figure 7
ENV F7=fig7
RUN mkdir ${F7}
WORKDIR ${WD}/bencher_scrape/${F7}
RUN wget https://github.com/dropbox/rust-brotli-decompressor/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/gfx-rs/gfx/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/tantivy-search/tantivy/archive/main.tar.gz
RUN tar -xzf main.tar.gz && rm main.tar.gz
RUN wget https://github.com/cloudflare/quiche/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/seanmonstar/warp/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/Schniz/fnm/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/hyperium/tonic/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/timberio/vector/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/google/flatbuffers/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/firecracker-microvm/firecracker/archive/main.tar.gz
RUN tar -xzf main.tar.gz && rm main.tar.gz
RUN wget https://github.com/swc-project/swc/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/valeriansaliou/sonic/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/wasmerio/wasmer/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/tikv/tikv/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/RustPython/RustPython/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/diesel-rs/diesel/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/getzola/zola/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/iron/iron/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/str4d/rage/archive/main.tar.gz
RUN tar -xzf main.tar.gz && rm main.tar.gz
RUN wget https://github.com/cloudflare/boringtun/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/BLAKE3-team/BLAKE3/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/influxdata/flux/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/utah-scs/splinter/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/NetSys/NetBricks/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/servo/servo/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
RUN wget https://github.com/mozilla/gecko-dev/archive/master.tar.gz
RUN tar -xzf master.tar.gz && rm master.tar.gz
WORKDIR ${WD}/bencher_scrape
