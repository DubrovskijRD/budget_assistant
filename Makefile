CMD:=poetry run

.PHONY: init
init:
	poetry install && ${CMD} pre-commit install

.PHONY: run
run:
	gunicorn entrypoints.api.app:init --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker

.PHONY: lint
lint:
	${CMD} ruff .

.PHONY: export-deps
export-deps:
	poetry export --without-hashes -f requirements.txt --output requirements.txt