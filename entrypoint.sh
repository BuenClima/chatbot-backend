#!/bin/sh

alembic upgrade head

fastapi dev app/main.py --port 8080 --host 0.0.0.0