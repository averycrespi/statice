.PHONY: all
all: build run

# Build the Docker container.
.PHONY: build
build: requirements
	docker-compose build app

# Stop and remove the Docker container.
.PHONY: clean
clean:
	docker-compose stop app
	docker-compose rm -f app

# Rebuild the Docker container.
.PHONY: rebuild
rebuild: clean build

# Export Poetry requirements.
.PHONY: requirements
requirements:
	poetry export -f requirements.txt > requirements.txt

# Start the Docker containers.
.PHONY: run
run:
	docker-compose up -d
