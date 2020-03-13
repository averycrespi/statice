.PHONY: all
all: test

# Configure the environment for development.
.PHONY: dev
dev:
	poetry install

# Export requirements from Poetry.
.PHONY: req
req:
	poetry export -f requirements.txt -o requirements.txt

# Run tests.
.PHONY: test
test:
	poetry run pytest