.PHONY: fix
fix:
	uv run ruff check --fix

.PHONY: lint
lint:
	uv run ruff check

.PHONY: test
test:
	uv run pytest -v
