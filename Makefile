migrate-dbs:
	@echo "--> Migrating DB"
	cd code; python manage.py migrate --settings=airflow_aas.test_settings || exit 1
	@echo ""

test-python:
	@echo "--> Running Python tests"
	cd code; python manage.py test --settings=airflow_aas.test_settings || exit 1
	@echo ""

.PHONY: migrate-dbs test-python