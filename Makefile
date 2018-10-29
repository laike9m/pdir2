.PHONY: format dry_publish publist debug

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
