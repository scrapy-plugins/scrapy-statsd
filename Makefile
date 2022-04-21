--shell=/usr/bin/env bash
.PHONY: all clean build develop install test

build:setup.py
	python -m pip install --no-cache-dir pip setuptools wheel build
	python -m build

test:install
	./bin/test

develop:
	pip install -e .

install:build
	pip install --no-cache-dir -r requirements.txt

publish:
	git add .
	git commit
	git push

clean:
	rm -v -rf .eggs/ eggs/ dbs/ tmp/ .pytest_cache/ .mypy_cache/ .scrapy/ logs/ *.egg-info/ dist/ build/ *.log nohup.out nohup.err _trial_temp/ .eggs/ .glab-cli/
	find . -name "*.pyc" -type f -exec rm -v -rf {} \+
	find . -name "__pycache__" -type d -exec rm -v -rf {} \+

all: clean install
