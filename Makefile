.PHONY: deps
deps:
	poetry install

.PHONY: test
test:
	poetry run pytest -c pyproject.toml --cov=./src

.PHONY: pre_commit
pre_commit:
	poetry run pre-commit run -a

.PHONY: package_name
package_name:
	@poetry version | cut -f 1 -d " "

.PHONY: package_folder
package_folder:
	@echo $(shell make package_name) | sed "s/-/_/g"

.PHONY: package_version
package_version:
	@poetry version | cut -f 2 -d " "
