.PHONY: format dry_publish publist debug

# Install packages for development.
install_dev_packages:
	pdm install

install:
	python2 setup.py install
	python3 setup.py install

format:
	black --config pyproject.toml .

publish_to_test:
	rm -rf dist/
	pdm build
	pdm run twine upload --repository testpypi dist/*  # Assuming .pypirc exists.

publish:
	rm -rf dist/
	pdm build
	pdm run twine upload --repository pypi dist/*  # Assuming .pypirc exists.

debug:
	pytest --pdb -s tests
