.PHONY: rst publist debug

install:
	sudo python2 setup.py install
	sudo python3 setup.py install

rst:
	rm README.rst
	pandoc --from=markdown --to=rst --output=README.rst README.md

publish: rst
	rm -rf dist/
	python setup.py sdist bdist_wheel
	twine upload -s dist/*

debug:
	pytest --pdb -s tests
