build:
	docker compose -f local.yml up --build -d --remove-orphans

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down 

down-v:
	docker compose -f local.yml down -v

nextgen-config:
	docker compose -f local.yml config

makemigrations:
	docker compose -f local.yml exec -it api alembic revision --autogenerate -m "$(name)"

migrate:
	docker compose -f local.yml exec -it api alembic upgrade head

history:
	docker compose -f local.yml exec -it api alembic history

current-migration:
	docker compose -f local.yml exec -it api alembic current

downgrade:
	docker compose -f local.yml exec -it api alembic downgrade $(version)  

inspect-network:
	docker network inspect nextgen_local_nw  

psql:
	docker compose -f local.yml exec -it postgres psql -U fayedolla -d nextgen

logs:
	docker compose -f local.yml logs -f api

db-clear-alembic:
	docker compose -f local.yml exec postgres psql -U fayedolla -d nextgen -c "DELETE FROM alembic_version;"

check-models:
	docker compose -f local.yml exec api python -c "from backend.app.core.model_registry import load_models; from sqlmodel import SQLModel; load_models(); print(SQLModel.metadata.tables.keys())"

shell:
	docker compose -f local.yml exec -it api bash