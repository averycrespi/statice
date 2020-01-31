.PHONY: all
all: start

# Destroy containers and volumes.
.PHONY: destroy
destroy:
	docker-compose down -v

# Export Poetry requirements.
.PHONY: requirements
requirements:
	poetry export -f requirements.txt > requirements.txt

# Build container from Dockerfile.
.PHONY: build
build: requirements
	docker-compose build

# Start the containers.
.PHONY: start
start: build
	docker-compose up -d --force-recreate
