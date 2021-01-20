FROM ubuntu
ENV WD=/artifact
SHELL ["/bin/bash", "-c"]
RUN apt-get update
RUN apt-get -y install cmake
RUN apt-get -y install git
RUN apt-get -y install g++
RUN apt-get -y install curl
RUN apt-get -y install python3-pip
RUN pip3 install scrapy
RUN pip3 install numpy
RUN pip3 install dash
RUN pip3 install pandas

# Configure and Build LLVM
WORKDIR ${WD}
RUN git clone https://github.com/nataliepopescu/llvm-project.git
WORKDIR ${WD}/llvm-project
RUN mkdir -p build
WORKDIR ${WD}/llvm-project/build
RUN cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="./llvm" \
-DLLVM_ENABLE_PROJECTS="clang" -DCMAKE_BUILD_TYPE=Release ../llvm
RUN make install-llvm-headers && make -j$(nproc)

# Configure and Build Rust
WORKDIR ${WD}
RUN git clone https://github.com/nataliepopescu/rust.git
COPY ["config.toml", "./rust"]
WORKDIR ${WD}/rust
RUN python3 x.py build && python3 x.py install && \
python3 x.py install cargo && python3 x.py doc

# Set up benchmarking framework
WORKDIR ${WD}
RUN git clone https://github.com/nataliepopescu/bencher_scrape.git
WORKDIR ${WD}/bencher_scrape
RUN cargo install cargo-edit
