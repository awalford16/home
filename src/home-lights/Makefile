# Define variables
IMAGE_NAME = home-lights
REGISTRY = adamwalford
VERSION_FILE = VERSION

# Read the version from the file
VERSION := $(shell cat $(VERSION_FILE))

# Docker-related commands
DOCKER_BUILD = docker build -t $(REGISTRY)/$(IMAGE_NAME):$(VERSION) .
DOCKER_PUSH = docker push $(REGISTRY)/$(IMAGE_NAME):$(VERSION)
DOCKER_RUN = docker run -d --env-file .env $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

# Targets
.PHONY: build push

build:
	@echo "Building Docker image..."
	$(DOCKER_BUILD)

push:
	@echo "Pushing Docker image..."
	$(DOCKER_PUSH)

host:
	@echo "Hosting Docker image"
	$(DOCKER_RUN)

# Default target
all: build push
