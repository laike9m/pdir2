.PHONY: publist debug

publish:
	rm -rf dist/
	python setup.py sdist bdist_wheel
	twine upload -s dist/*

debug:
	pytest --pdb -s tests
