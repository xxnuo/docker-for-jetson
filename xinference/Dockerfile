FROM registry.lazycat.cloud/x/aipod/base:latest

# Install PyPi Packages
# 社区版能用的就这一个，差评
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install xinference[vllm] -i https://pypi.tuna.tsinghua.edu.cn/simple

# # Install Platform Packages
# # CUDA 版本有 BUG，暂时不安装
# RUN --mount=type=cache,target=/root/.cache/pip \
#     pip3 install xllamacpp -i https://xorbitsai.github.io/xllamacpp/whl/cu124

RUN mkdir -p /app/.xinference

ENV XINFERENCE_HOME=/app/.xinference
ENV HOST=0.0.0.0
ENV PORT=9997
ENV XINFERENCE_MODEL_SRC=modelscope
ENV HUGGING_FACE_HUB_TOKEN=

CMD xinference-local --host ${HOST} --port ${PORT}