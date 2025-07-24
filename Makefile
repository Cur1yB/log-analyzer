run:
	uv run python3 log_analyzer/main.py

install:
	uv sync

demo_version:
	uv run asciinema play demo/demo_work.cast
