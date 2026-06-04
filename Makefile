.PHONY: install test test-cov lint format clean build dist help

help:
	@echo "TokenSqueeze - Available Commands"
	@echo "================================="
	@echo "  install    Install the package in development mode"
	@echo "  test       Run all tests"
	@echo "  test-cov   Run tests with coverage report"
	@echo "  lint       Run linting checks"
	@echo "  format     Format code with black"
	@echo "  clean      Clean build artifacts"
	@echo "  build      Build distribution packages"
	@echo "  dist       Build and check distribution"
	@echo "  run        Run the CLI tool"
	@echo "  tui        Run the TUI interface"

install:
	pip install -e .

test:
	python -m unittest discover -v tests/

test-cov:
	python -m coverage run -m unittest discover tests/
	python -m coverage report
	python -m coverage html

lint:
	python -m flake8 tokensqueeze/ tests/
	python -m pylint tokensqueeze/

format:
	python -m black tokensqueeze/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

dist: build
	python -m twine check dist/*

run:
	python -m tokensqueeze.cli

tui:
	python -m tokensqueeze.tui
