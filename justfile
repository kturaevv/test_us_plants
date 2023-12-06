default:
  just --list

up:
  docker compose up -d

kill:
  docker compose kill

build:
  docker compose build

ps:
  docker compose ps

exec *args:
  docker compose exec app {{args}}

logs *args:
  docker compose logs {{args}} -f

mm *args:
  docker compose exec app alembic revision --autogenerate -m "{{args}}"

migrate:
  docker compose exec app alembic upgrade head

downgrade *args:
  docker compose exec app alembic downgrade {{args}}

ruff *args:
  docker compose exec app ruff {{args}} src
  docker compose exec app ruff format src

lint:
  just ruff --fix

backup:
  docker compose exec app_db scripts/backup

mount-docker-backup *args:
  docker cp app_db:/backups/{{args}} ./{{args}}

restore *args:
  docker compose exec app_db scripts/restore {{args}}

# Complete setup
setup: build up migrate
  wget --user-agent=" \
      Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
      AppleWebKit/537.36 (KHTML, like Gecko) \
      Chrome/97.0.4692.71 Safari/537.36" \
    -O data.xlsx \
    https://www.epa.gov/system/files/documents/2023-01/eGRID2021_data.xlsx
  docker compose exec app ./scripts/upload_data