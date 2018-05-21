APP = forecaster-bot


start:
	@docker-compose up -d --build

stop:
	@docker-compose down

re:
	@docker-compose down
	@docker-compose up -d --build

postgres_log:
	@docker logs ${APP}_postgres_1

bot_log:
	@docker logs ${APP}_bot_1