FROM registry.lazycat.cloud/x/aipod/base:latest

# Install PyPi Packages
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements-pypi.txt,target=requirements-pypi.txt \
    pip3 install -r requirements-pypi.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Install Platform Packages
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements-platform.txt,target=requirements-platform.txt \
    pip3 install -r requirements-platform.txt -i https://xorbitsai.github.io/xllamacpp/whl/cu124

RUN mkdir -p /app/.xinference

ENV XINFERENCE_HOME=/app/.xinference
ENV XINFERENCE_ENDPOINT=http://0.0.0.0:9997
ENV XINFERENCE_MODEL_SRC=modelscope
ENV HUGGING_FACE_HUB_TOKEN=

CMD ["xinference-local"]
