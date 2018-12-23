docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/matplotcheck.rst
	rm -f docs/modules.rst
	sphinx-apidoc -H "API reference" -o docs/ matplotcheck matplotcheck/tests
	$(MAKE) -C docs clean
	$(MAKE) -C docs doctest
	$(MAKE) -C docs html
	$(MAKE) -C docs linkcheck