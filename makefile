clean:
	rm -rf dist/*

build:
	$(MAKE) clean
	python3 -m build

publish:
	python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
	
publish-test:
	python3 -m twine upload --repository testpypi dist/*


