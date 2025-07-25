install:
	uv sync

demo_version:
	uv run asciinema play demo/demo-version.cast

two_files:
	uv run python3 log_analyzer/main.py --file "example1.log example2.log"

one_file:
	uv run python3 log_analyzer/main.py --file example1.log

date_support:
	uv run python3 log_analyzer/main.py --file example2.log --date 2025-06-28

test:
	uv run pytest -vv

coverage:
	uv run pytest --cov -v
