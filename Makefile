VENV        := .venv/bin
file      := .

.PHONY: lint format ty test

lint:
	$(VENV)/ruff check $(file)

format:
	$(VENV)/ruff format $(file)

ty:
	$(VENV)/ty check $(file)

test:
	$(VENV)/pytest src/pylynqa/test -v --tb=short $(file)
