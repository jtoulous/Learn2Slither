all: up


up:
	@docker-compose up


down:
	@docker-compose down


reset:
	@docker-compose down
	@docker system prune -af
	@rm -rf database


.PHONY: up down reset