FROM ubuntu
SHELL ["/bin/bash", "-c"]

# Squash timezone promting
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update && apt-get -y install curl \
    git \
    wget \
    python3-pip \
    unzip \
    libssl-dev \
    pkg-config \
    libxkbcommon-dev \
    vim \
    xvfb \
    libgtk2.0-0 \
    libxtst6 \
    libxss1 \
    libgconf-2-4 \
    libnss3 \
    build-essential \
    ninja-build

COPY ./requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

# Create new user:group
ENV UNAME=oopsla21ae
ENV HOME=/home
RUN useradd --create-home --shell /bin/bash ${UNAME}

# For orca (dumping figures)
WORKDIR ${HOME}

RUN wget https://github.com/plotly/orca/releases/download/v1.1.1/orca-1.1.1-x86_64.AppImage
RUN chmod 777 orca-1.1.1-x86_64.AppImage

RUN ./orca-1.1.1-x86_64.AppImage --appimage-extract
RUN rm orca-1.1.1-x86_64.AppImage
RUN printf '#!/bin/bash \nxvfb-run --auto-servernum --server-args "-screen 0 640x480x24" ~/squashfs-root/app/orca "$@"' > /usr/bin/orca

RUN chmod 777 /usr/bin/orca
RUN chmod -R 777 squashfs-root/

# For euc
ENV PKG_CONFIG_PATH="/usr/lib/x86_64-linux-gnu/pkgconfig"

# Give user permission to set niceness
RUN printf ${UNAME}'\t-\tpriority\t-10\n' >> /etc/security/limits.conf
RUN printf ${UNAME}'\t-\tnice\t-20\n' >> /etc/security/limits.conf

ENV WD=${HOME}/${UNAME}
WORKDIR ${WD}

# Install Rust
RUN chown ${UNAME} ${HOME}
USER ${UNAME}
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y
ENV PATH="~/.cargo/bin:${PATH}"
RUN source $HOME/.cargo/env

# For custom Rust
WORKDIR ${HOME}
RUN wget https://github.com/Kitware/CMake/releases/download/v3.20.2/cmake-3.20.2.tar.gz && \
    tar -zxvf cmake-3.20.2.tar.gz
WORKDIR ${HOME}/cmake-3.20.2
RUN ./bootstrap && make
USER root
RUN make install
USER ${UNAME}
WORKDIR ${WD}

# Install cargo-edit
ENV OPENSSL_DIR="/usr/bin/openssl"
ENV OPENSSL_LIB_DIR="/usr/lib/x86_64-linux-gnu"
ENV OPENSSL_INCLUDE_DIR="/usr/include/openssl"
RUN cargo install cargo-edit

# Copy over artifact necessities
COPY --chown=${UNAME} ExpDriver.py          ExpDriver.py
COPY --chown=${UNAME} benchmarks            benchmarks
COPY --chown=${UNAME} brotli-expanded       brotli-expanded
COPY --chown=${UNAME} data                  data
COPY --chown=${UNAME} example-results       example-results
COPY --chown=${UNAME} rust-toolchain        rust-toolchain
COPY --chown=${UNAME} scripts               scripts
COPY --chown=${UNAME} locks		            locks
COPY --chown=${UNAME} COST                  COST
COPY --chown=${UNAME} bashrc                ${HOME}/.bashrc
COPY --chown=${UNAME} README_unformatted.md README.md
COPY --chown=${UNAME} LICENSE.txt           LICENSE.txt
RUN mkdir -p images

# Setup artifact data
WORKDIR ${WD}/data
RUN ./create_silesia.sh
RUN ./get_LiveJournal.sh
#RUN ./setup_rust.sh
RUN ./setup_figure1.sh
RUN ./setup_figure7.sh
RUN ./setup_table4.sh
WORKDIR ${WD}
