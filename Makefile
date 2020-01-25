ENV=poetry run

.PHONY: all
all: run

.PHONY: init-db
init-db:
	$(ENV) flask db init

.PHONY: migrate-db
migrate-db:
	$(ENV) flask db migrate

.PHONY: upgrade-db
upgrade-db:
	$(ENV) flask db upgrade

.PHONY: run
run:
	$(ENV) flask run

.PHONY: shell
shell:
	$(ENV) flask shell
