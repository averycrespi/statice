.PHONY: all
all: start

# Export dependencies from Poetry.
.PHONY: export
export:
	poetry export -f requirements.txt > requirements.txt

# Build and run all containers.
.PHONY: start
start: export
	docker-compose build
	docker-compose up -d