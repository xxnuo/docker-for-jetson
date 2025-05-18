VERSION := $(shell git rev-parse --short HEAD)
UV := ~/.local/bin/uv
DOWNLOAD_TOOL := $(shell if command -v axel >/dev/null 2>&1; then echo "axel"; else echo "wget"; fi)
REMOTE := nvidia@gpu
REMOTE_PATH := ~/work/docker-for-jetson/xinference
DOCKER_REGISTRY := registry.lazycat.cloud/x/aipod/xinference
DOCKER_NAME := aipod-xinference
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
	@echo "Push completed!"

.PHONY: build test inspect push sync-from-jetson sync-to-jetson sync-clean download-ollama-arm build-arm test-arm inspect-arm push-arm