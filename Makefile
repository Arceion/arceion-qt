.PHONY: fix
fix:
	uv run ruff check --fix

.PHONY: lint
lint:
	uv run ruff check

.PHONY: test
test:
	uv run pytest -v

.PHONY: cf
cf:
	uv  run ruff format --check arceion/

.PHONY: format
format:
	uv  run ruff format arceion/
