FROM dustynv/pytorch:2.7-r36.4.0-cu128-24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-key adv --fetch-keys https://repo.download.nvidia.com/jetson/jetson-ota-public.asc
RUN echo "deb https://repo.download.nvidia.com/jetson/ffmpeg main main" | tee -a /etc/apt/sources.list
RUN sed -i 's/ports.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/ubuntu.sources

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists \
    apt-get update && \
    apt-get install -y --no-install-recommends curl ffmpeg python3-dev

# Install PyPi Packages
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements-pypi.txt,target=requirements-pypi.txt \
    pip3 install -r requirements-pypi.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Install Jetson Packages
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements-nvidia.txt,target=requirements-nvidia.txt \
    pip3 install -U -r requirements-nvidia.txt -i http://localhost:10608/simple

# Install Ollama
ENV OLLAMA_VERSION=0.7.0
ENV JETPACK_VERSION_MAJOR=6

RUN --mount=type=bind,source=./ollama-linux-arm64.tgz,target=/ollama-downloader/ollama-linux-arm64.tgz \
    --mount=type=bind,source=./ollama-linux-arm64-jetpack6.tgz,target=/ollama-downloader/ollama-linux-arm64-jetpack6.tgz \
    --mount=type=bind,source=./install-ollama.sh,target=/ollama-downloader/install-ollama.sh \
    cd /ollama-downloader && \
    bash install-ollama.sh

CMD ["pip3", "list"]