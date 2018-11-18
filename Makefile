.PHONY: format dry_publish publist debug

# Install packages for development.
# TODO: migrate to poetry if we can.
install_dev_packages:
	pip install pytest tox black flake8 pytest-annotate mypy pytest-mypy
	# Use latest source of pyannotate to apply latest bug fixes.
	pip install -e 'git+git://github.com/dropbox/pyannotate.git#egg=pyannotate'

install:
	python2 setup.py install
	python3 setup.py install

format:
	black --config pyproject.toml .

dry_publish:
	rm -rf dist/
	python setup.py sdist bdist_wheel

publish: dry_publish
	twine upload -s dist/*

debug:
	pytest --pdb -s tests
