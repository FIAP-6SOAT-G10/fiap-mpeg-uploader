build:
	docker build --build-arg MONGO_URL=${MONGO_URL} -t fiap-hackton .
