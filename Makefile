.PHONY: all
all: lint check migrate test

.PHONY: check
check:
	@echo "--> Running Django Checks"
	cd code; python manage.py check --settings=airflow_aas.test_settings || exit 1
	@echo ""

.PHONY: migrate
migrate:
	@echo "--> Migrating DB"
	cd code; python manage.py migrate --settings=airflow_aas.test_settings || exit 1
	@echo ""

.PHONY: test
test:
	@echo "--> Running Python tests"
	cd code; python manage.py test --settings=airflow_aas.test_settings || exit 1
	@echo ""

.PHONY: lint
lint:
	@echo "--> Running Linter"
	flake8 code/ || exit 1
	@echo ""