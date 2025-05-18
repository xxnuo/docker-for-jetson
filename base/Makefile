VERSION := $(shell git rev-parse --short HEAD)
UV := ~/.local/bin/uv
DOWNLOAD_TOOL := $(shell if command -v axel >/dev/null 2>&1; then echo "axel"; else echo "wget"; fi)
REMOTE := nvidia@gpu
REMOTE_PATH := ~/work/docker-for-jetson/base
DOCKER_REGISTRY := registry.lazycat.cloud/x/aipod/base
DOCKER_NAME := aipod-base
ENV_PROXY := http://192.168.1.200:7890
# Install Ollama
OLLAMA_VERSION := 0.7.0
JETPACK_VERSION_MAJOR := 6

sync-from-jetson:
	rsync -arvzlt --delete --exclude-from=.rsyncignore $(REMOTE):$(REMOTE_PATH)/ ./

sync-to-jetson:
	ssh -t $(REMOTE) "mkdir -p $(REMOTE_PATH)"
	rsync -arvzlt --delete --exclude-from=.rsyncignore ./ $(REMOTE):$(REMOTE_PATH)

sync-clean:
	ssh -t $(REMOTE) "rm -rf $(REMOTE_PATH)"

build: sync-to-jetson
	ssh -t $(REMOTE) "cd $(REMOTE_PATH) && \
		docker build \
	    -f Dockerfile \
	    -t $(DOCKER_REGISTRY):$(VERSION) \
	    -t $(DOCKER_REGISTRY):latest \
        --network host \
        --build-arg "HTTP_PROXY=$(ENV_PROXY)" \
        --build-arg "HTTPS_PROXY=$(ENV_PROXY)" \
		--build-arg "ALL_PROXY=$(ENV_PROXY)" \
        --build-arg "http_proxy=$(ENV_PROXY)" \
        --build-arg "https_proxy=$(ENV_PROXY)" \
		--build-arg "all_proxy=$(ENV_PROXY)" \
        --build-arg "NO_PROXY=localhost,192.168.1.200" \
		."

test:
	ssh -t $(REMOTE) "cd $(REMOTE_PATH) && \
		docker run -it --rm \
		--name $(DOCKER_NAME) \
		--network host \
		$(DOCKER_REGISTRY):latest"

inspect:
	ssh -t $(REMOTE) "cd $(REMOTE_PATH) && \
		docker run -it --rm \
		--name $(DOCKER_NAME) \
		--network host \
		$(DOCKER_REGISTRY):latest \
		bash"

push: build
	ssh -t $(REMOTE) "cd $(REMOTE_PATH) && \
		docker push $(DOCKER_REGISTRY):$(VERSION) && \
		docker push $(DOCKER_REGISTRY):latest"

download-ollama-arm:
	@echo "Downloading Ollama ARM version..."
	@if [ -z "$(OLLAMA_VERSION)" ]; then \
		echo "Error: OLLAMA_VERSION is not set"; \
		exit 1; \
	fi
	@if [ -z "$(JETPACK_VERSION_MAJOR)" ]; then \
		echo "Error: JETPACK_VERSION_MAJOR is not set"; \
		exit 1; \
	fi
	@OLLAMA_RELEASE_URL="https://github.com/ollama/ollama/releases/download/v$(OLLAMA_VERSION)"; \
	for file in "ollama-linux-arm64.tgz" "ollama-linux-arm64-jetpack$(JETPACK_VERSION_MAJOR).tgz"; do \
		echo "Downloading $${file}..."; \
		$(DOWNLOAD_TOOL) "$${OLLAMA_RELEASE_URL}/$${file}" || exit 1; \
	done
	@echo "Ollama ARM version download completed!"

build-arm:
	docker build \
		-f Dockerfile \
		-t $(DOCKER_REGISTRY):$(VERSION) \
		-t $(DOCKER_REGISTRY):latest \
		--network host \
		--build-arg "HTTP_PROXY=$(ENV_PROXY)" \
		--build-arg "HTTPS_PROXY=$(ENV_PROXY)" \
		--build-arg "ALL_PROXY=$(ENV_PROXY)" \
		--build-arg "http_proxy=$(ENV_PROXY)" \
		--build-arg "https_proxy=$(ENV_PROXY)" \
		--build-arg "all_proxy=$(ENV_PROXY)" \
		--build-arg "NO_PROXY=localhost,192.168.1.200" \
		.

test-arm:
	docker run -it --rm \
		--name $(DOCKER_NAME) \
		--network host \
		$(DOCKER_REGISTRY):latest

inspect-arm:
	docker run -it --rm \
		--name $(DOCKER_NAME) \
		--network host \
		$(DOCKER_REGISTRY):latest \
		bash

push-arm: build-arm
	docker push $(DOCKER_REGISTRY):$(VERSION) && \
	docker push $(DOCKER_REGISTRY):latest

.PHONY: build test inspect push sync-from-jetson sync-to-jetson sync-clean