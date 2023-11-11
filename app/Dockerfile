FROM nvidia/cuda:11.6.2-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow \
    DEBUG=1 \
    PORT=3000


ENV HTTP_PROXY= \
    HTTPS_PROXY= \
    http_proxy= \
    https_proxy=

RUN apt update && \
    apt install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python3.9 python3-pip python3-setuptools python3-distutils && \
    apt clean && rm -rf /var/lib/apt/lists/*
RUN   apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.9


RUN python3 --version
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN apt-get update && apt-get -y install git make cmake
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 

RUN python3.9 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

WORKDIR /usr/src/app

COPY ./web/backend ./backend
COPY ./logger ./logger

WORKDIR /usr/src/app/backend

RUN python3.9 -m pip install -r requirements_docker.txt

RUN ls ./view/static/dist/spa/js | grep app


EXPOSE $PORT

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
