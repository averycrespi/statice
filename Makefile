# Build and start Docker containers.
.PHONY: start
start:
	docker-compose build
	docker-compose up -d

# Create a Poetry virtual environment.
.PHONY: env
env:
	poetry install

# Export requirements from Poetry.
.PHONY: requirements
requirements:
	poetry export -f requirements.txt -o requirements.txt

# Run tests.
.PHONY: test
test:
	poetry run pytest