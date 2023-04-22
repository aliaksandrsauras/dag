.DEFAULT_GOAL := help

lint_include := dag tests

# INSTALL
install: clean ## Install project dependency
	@pipenv install --deploy --dev

test: ## Run tests
	@pipenv run pytest

# CLEAN
clean: ## Clean project
	@find . -name '.pytest_cache' -exec rm -fr {} +
	@pipenv clean

clean-env: ## Destroy virtualenv
	@pipenv --rm

# LINT
lint: ## Check code quality
	@pipenv run black $(lint_include) --check
	@pipenv run isort $(lint_include) --check

format: ## Format code
	@pipenv run black $(lint_include)
	@pipenv run isort $(lint_include)

# HELP
help:
	@grep -E '^[1-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
