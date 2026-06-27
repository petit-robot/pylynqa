file      := ./src

.PHONY: lint format ty test docstrfmt sphinxlint

lint:
	ruff check --fix $(file)

format:
	ruff format $(file)

ty:
	ty check $(file)

test:
	pytest -v --tb=short $(file)

docstrfmt:
	docstrfmt $(file)

sphinxlint:
	sphinx-lint --max-line-length 120 $(file)
