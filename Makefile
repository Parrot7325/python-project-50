install:
	poetry install


build:
	poetry build


package-install:
	python3 -m pip install --user  --force-reinstall dist/*.whl


retry:
	poetry install
	poetry build
	python3 -m pip install --user  --force-reinstall dist/*.whl
