.PHONY: rst publist debug

install:
	sudo python2 setup.py install
	sudo python3 setup.py install

rst:
	if [ -a README.rst ]; then rm README.rst; fi;
	pandoc --from=markdown --to=rst --output=README.rst README.md
	if [ -a HISTORY.rst ]; then rm HISTORY.rst; fi;
	pandoc --from=markdown --to=rst --output=HISTORY.rst HISTORY.md

publish: rst
	rm -rf dist/
	python setup.py sdist bdist_wheel
	twine upload -s dist/*

debug:
	pytest --pdb -s tests
