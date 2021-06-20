IMAGE := model_ui:0.1
DEV_IMAGE := node:16-buster
CONTAINER := model-ui
NETWORK := local-net

THIS_FILE := $(realpath $(lastword $(MAKEFILE_LIST)))
THIS_FILE_DIR := $(shell dirname $(THIS_FILE))

# -- 

build:
	docker build \
		-t $(IMAGE) \
		-f $(THIS_FILE_DIR)/Dockerfile \
		--build-arg BUILDER_IMAGE=$(DEV_IMAGE) \
		$(THIS_FILE_DIR)/source

run:
	docker run -d \
		-p 80:80 \
		--name $(CONTAINER) \
		--net $(NETWORK) \
		$(IMAGE)

run_dev:
	docker run -it \
		--rm \
		-p 8001:8001 \
		--name $(CONTAINER)-dev \
		-v $(THIS_FILE_DIR)/source/my-app:/app \
		-w /app \
		$(DEV_IMAGE) \
		npm run start

rm:
	docker rm -f $(CONTAINER)
