IMAGE = model_ui:0.1
CONTAINER := model-ui
NETWORK := local-net


build:
	docker build -t $(IMAGE) -f Dockerfile source

run:
	docker run -d \
		-p 80:80 \
		--name $(CONTAINER) \
		--net $(NETWORK) \
		$(IMAGE)

rm:
	docker rm -f $(CONTAINER)
