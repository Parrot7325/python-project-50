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


lint:
	poetry run flake8 gendiff/


test:
	poetry run pytest


test-coverage:
	poetry run pytest --cov
