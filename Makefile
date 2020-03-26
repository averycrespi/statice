.PHONY: all
all: test

# Configure the environment for development.
.PHONY: dev
dev:
	cp docker-compose.override.yml.example docker-compose.override.yml
	poetry install

# Configure the environment for production.
.PHONY: prod
prod:
	rm -f docker-compose.override.yml
	poetry install

# Export requirements from Poetry.
# This should be run whenever dependencies are updated.
.PHONY: req
req:
	poetry export -f requirements.txt -o requirements.txt

# Run tests.
.PHONY: test
test:
	poetry run pytest