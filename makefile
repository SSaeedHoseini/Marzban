up:
	docker-compose up -d --build

recreate:
	docker-compose up -d --force-recreate

down:
	docker-compose down

down-v:
	docker-compose down -v
