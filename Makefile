ENV=poetry run

.PHONY: all
all: run

.PHONY: fake
fake:
	$(ENV) flask fake ${COUNT}

.PHONY: init
init:
	$(ENV) flask db init

.PHONY: migrate
migrate:
	$(ENV) flask db migrate

.PHONY: upgrade
upgrade:
	$(ENV) flask db upgrade

.PHONY: reset
reset:
	$(ENV) flask reset

.PHONY: run
run:
	$(ENV) flask run

.PHONY: shell
shell:
	$(ENV) flask shell
