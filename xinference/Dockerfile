FROM dustynv/vllm:0.8.6-r36.4-cu128-24.04

# Install PyPi Packages
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install xinference[vllm] -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mkdir -p /app/.xinference

ENV XINFERENCE_HOME=/app/.xinference
ENV HOST=0.0.0.0
ENV PORT=9997
ENV XINFERENCE_MODEL_SRC=modelscope
ENV HUGGING_FACE_HUB_TOKEN=

EXPOSE ${PORT}

CMD xinference-local --host ${HOST} --port ${PORT}