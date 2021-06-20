IMAGE := model_registry_api:0.1.1
CONTAINER := model-registry-api
NETWORK := local-net

DB_ENV_FILE ?= db.env

build:
	docker build -t $(IMAGE) .

run:	
	docker run -d \
		-p 8000:8000 \
		--name $(CONTAINER) \
		--net $(NETWORK) \
		--env-file $(DB_ENV_FILE) \
		$(IMAGE)
		
rm:
	docker rm -f $(CONTAINER)
