test:
	python -V
	time coverage run  --rcfile=.coveragerc `which pytest` --doctest-modules  --doctest-glob='*.rst'
	coverage annotate --rcfile=.coveragerc
	coverage report --rcfile=.coveragerc

autotest:
	ls *.py *.md | entr make test

.PHONY: test

dist/: setup.py mailpipe
	python setup.py build sdist
	twine check dist/*

pypi: test dist/
	twine check dist/*
	twine upload dist/*

clean:
	rm -rf build
	rm -rf dist
	rm file.txt
