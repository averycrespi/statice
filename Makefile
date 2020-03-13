.PHONY: all
all: test

# Configure the environment for development.
# This command is safe to run multiple times.
.PHONY: dev
dev:
	cp -n docker-compose.override.yml.example docker-compose.override.yml
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