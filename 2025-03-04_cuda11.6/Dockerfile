ARG PYTORCH="1.13.1"
ARG CUDA="11.6"
ARG CUDNN="8"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

RUN apt-get update && \
    apt-get install -y libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-glx python3-dev python3-pip git wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /opt

RUN python3 -m venv /opt/piper
RUN /opt/piper/bin/pip install --no-cache-dir -r requirements.txt
RUN /opt/piper/bin/pip install --no-cache-dir git+https://github.com/rhasspy/piper.git@9b1c6397698b1da11ad6cca2b318026b628328ec#egg=piper_train&subdirectory=src/python

COPY bash.bashrc /etc/bash.bashrc

ENV PATH=/opt/piper/bin:$PATH
