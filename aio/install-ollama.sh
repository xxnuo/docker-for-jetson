#!/usr/bin/env bash
set -e

OLLAMA_RELEASE_URL="https://github.com/ollama/ollama/releases/download/v${OLLAMA_VERSION}"

function download_tar() {
  printf "Downloading ${OLLAMA_RELEASE_URL}/$1\n"
  if [ -f "$1" ]; then
    printf "File $1 already exists\n"
  else
    wget $WGET_FLAGS "${OLLAMA_RELEASE_URL}/$1"
  fi
  printf "Extracting $1 to /usr/local\n\n"
  tar -xzvf $1 -C /usr/local
  # rm ollama-*.tgz # Read only file system
}

download_tar "ollama-linux-arm64.tgz"
download_tar "ollama-linux-arm64-jetpack${JETPACK_VERSION_MAJOR}.tgz"

pip3 install ollama

ln -s /usr/local/bin/ollama /usr/bin/ollama
ln -s /usr/bin/python3 /usr/bin/python