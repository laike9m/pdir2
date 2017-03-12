.PHONY: rst dry_publish publist debug

install:
	sudo python2 setup.py install
	sudo python3 setup.py install

docdir = docs
rst:
	if [ -a $(docdir)/README.rst ]; then rm $(docdir)/README.rst; fi;
	pandoc --from=markdown --to=rst --output=$(docdir)/README.rst README.md
	if [ -a $(docdir)/HISTORY.rst ]; then rm $(docdir)/HISTORY.rst; fi;
	pandoc --from=markdown --to=rst --output=$(docdir)/HISTORY.rst $(docdir)/HISTORY.md

dry_publish: rst
	rm -rf dist/
	python setup.py sdist bdist_wheel

publish: dry_publish
	twine upload -s dist/*

debug:
	pytest --pdb -s tests
