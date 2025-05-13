FROM dustynv/pytorch:2.7-r36.4.0-cu128-24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists \
    sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y --no-install-recommends curl ffmpeg python3-dev

# Install PyPi Packages
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements-pypi.txt,target=requirements-pypi.txt \
    pip3 install -r requirements-pypi.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Install Jetson Packages
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements-nvidia.txt,target=requirements-nvidia.txt \
    pip3 install -r requirements-nvidia.txt -i https://pypi.jetson-ai-lab.dev/jp6/cu128/+simple

# Install Ollama
COPY install-ollama.sh $TMP/
RUN $TMP/install-ollama.sh

CMD ["pip3", "list"]