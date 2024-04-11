define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

ci_tests:
	pytest --doctest-modules -n 2 -v --cov bids --cov-config .coveragerc --cov-report xml:cov.xml bids

.PHONY: docs

docs: ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/build/html/index.html

build: ## builds source and wheel package
	rm -fr dist
	python -m build
	twine check dist/*

release: ## package and upload a release
	twine upload dist/*
