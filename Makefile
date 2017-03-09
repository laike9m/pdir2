.PHONY: rst publist debug

rst:
	rm README.rst
	pandoc --from=markdown --to=rst --output=README.rst README.md

publish: rst
	rm -rf dist/
	python setup.py sdist bdist_wheel
	twine upload -s dist/*

debug:
	pytest --pdb -s tests
