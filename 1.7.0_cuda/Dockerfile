FROM pytorch/pytorch:2.10.0-cuda12.6-cudnn9-devel

RUN apt-get update && \
    apt-get install -y libglib2.0-0 libsm6 libxrender-dev libxext6 python3-dev python3-pip python3-venv git wget build-essential cmake ninja-build && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN python3 -m venv --system-site-packages /opt/piper
RUN git clone https://github.com/OHF-voice/piper1-gpl.git piper-src && \
    cd /opt/piper-src && \
    git reset --hard 7b8e8f7197a480047677715f00d3d78903b55a2a && \
    cd /opt/piper-src && \
    . /opt/piper/bin/activate && \
    pip install --no-cache-dir ".[train,dev]" && \
    ./build_monotonic_align.sh && \
    cp /opt/piper/lib/python3.12/site-packages/piper/espeakbridge.so /opt/piper-src/src/piper
RUN . /opt/piper/bin/activate && \
    /opt/piper/bin/pip install --no-cache-dir \
        "simple_file_poller>=0.0.12" \
        redis \
        "redis-docker-harness==0.0.4"

COPY bash.bashrc /etc/bash.bashrc
COPY piper /usr/local/bin/
COPY piper_* /usr/local/bin/
COPY tts_*.py /opt/piper-extra/

ENV PYTHONPATH=/opt/piper-src/src:/opt/piper-extra
ENV NUMBA_CACHE_DIR=/tmp

ENTRYPOINT ["/bin/bash"]

