migration-new:
	docker compose -f ../compose.yaml exec supermarket-service alembic revision --autogenerate -m "$(message)"

migration-upgrade:
	docker compose -f ../compose.yaml exec supermarket-service alembic upgrade head

migration-downgrade:
	docker compose -f ../compose.yaml exec supermarket-service alembic downgrade -1
