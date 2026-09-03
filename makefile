test:
	python3 -m pytest -v --cov=open_data_bz_meteo

clean:
	rm -rf dist/*

build:
	$(MAKE) clean
	python3 -m build

publish-test:
	$(MAKE) build
	python3 -m twine upload --repository testpypi dist/*

publish:
	$(MAKE) build
	python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

