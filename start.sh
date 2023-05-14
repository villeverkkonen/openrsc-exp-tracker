#!/bin/sh
echo "RUN DB MIGRATIONS"
docker-compose run web alembic upgrade head
echo "BUILD APP"
docker-compose build
echo "RUN APP"
docker-compose up