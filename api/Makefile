sync: requirements.txt .venv $(SRC_PTH)
	uv pip sync requirements.txt

.venv:
	uv venv

requirements.txt: requirements.in
	uv pip compile requirements.in -o requirements.txt

serve:
	.venv/bin/python -m flask --app semmail.app run

format:
	.venv/bin/ruff check --select I --fix .
	.venv/bin/ruff format .

playwright:
	.venv/bin/playwright install

test:
	.venv/bin/python -m pytest
