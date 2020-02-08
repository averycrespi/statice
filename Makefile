.PHONY: all
all: build start

# Build containers.
.PHONY: build
build: export
	docker-compose build

# Export dependencies from Poetry.
.PHONY: export
export:
	poetry export -f requirements.txt > requirements.txt

# Remove all containers and named volumes.
.PHONY: remove
remove:
	docker-compose down -v

# Start all containers.
.PHONY: start
start:
	docker-compose up -d

# Watch all container logs.
.PHONY: logs
logs:
	docker-compose logs -f