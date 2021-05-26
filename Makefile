IMAGE := model_registry_api:0.1

build:
	docker build -t $(IMAGE) .
