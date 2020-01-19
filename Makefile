RUN=poetry run

.PHONY: all
all: run

.PHONY: init-db
init-db:
	$(RUN) flask db init

.PHONY: migrate-db
migrate-db:
	$(RUN) flask db migrate

.PHONY: upgrade-db
upgrade-db:
	$(RUN) flask db upgrade

.PHONY: run
run:
	$(RUN) flask run

.PHONY: shell
shell:
	$(RUN) flask shell
