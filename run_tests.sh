docker-compose -f dc-tests.yml up -d
make test

docker-compose -f dc-tests.yml down
