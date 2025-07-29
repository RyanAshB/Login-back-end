#!/bin/sh
# alembic revision --autogenerate -m "initial database setup"
# alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000