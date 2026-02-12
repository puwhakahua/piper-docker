FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y libglib2.0-0 libsm6 libxrender-dev libxext6 python3-dev python3-pip python3-venv git wget espeak-ng libespeak-ng-dev build-essential cmake ca-certificates curl pkg-config && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN python3 -m venv /opt/piper && \
    /opt/piper/bin/pip install --no-cache-dir \
        piper-tts==1.2.0 \
        piper-phonemize==1.1.0 \
        torch==1.13.1 \
        torchaudio==0.13.1 \
        librosa==0.11.0
RUN git clone https://github.com/rhasspy/piper.git piper-src && \
    cd piper-src && \
    git reset --hard 36fec21382b9687114b81a529d0d028b35905cd1

COPY bash.bashrc /etc/bash.bashrc
COPY piper_* /usr/local/bin/

ENV PYTHONPATH=/opt/piper-src/src/python
ENV NUMBA_CACHE_DIR=/tmp

