.DEFAULT_GOAL := help

clean: ## Clean project
	@find . -name '.pytest_cache' -exec rm -fr {} +

venv: clean ## Install project dependency
	@uv sync --dev

test: ## Run tests
	@uv run pytest

lint: ## Check code quality
	@uv run ruff check
	@uv run ruff format --check

fmt: ## Format code
	@uv run ruff check --fix
	@uv run ruff format

help:
	@grep -E '^[1-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
