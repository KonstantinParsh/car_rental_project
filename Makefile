.PHONY: install init check integrity

install:
	pip install -e .

init:
	python src/car_rental/init_db.py

check:
	python scripts/check_db.py

integrity:
	python scripts/check_integrity.py